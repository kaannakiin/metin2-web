#!/usr/bin/env python3
"""Private, uncached client preview. No package step, CDN or production writes."""

import argparse
import functools
import gzip
import hashlib
import http.server
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import parse_qs, unquote, urlsplit


PAGE_FILES = ('client.html', 'client.js', 'client.wasm', 'client.data', 'preload.js')
PAGE = re.compile(r'/(?:client\.(?:html|js|wasm|data)|preload\.js|'
                  r'client\.locale_[a-zA-Z0-9_-]+\.(?:data|js))\Z')
CORPUS = re.compile(r'/corpus/(?:[a-f0-9]{32}\.bin|manifest\.bin|groups\.txt)\Z')


def snapshot(port, destination, bridge_port):
    port, destination = Path(port), Path(destination)
    for name in PAGE_FILES:
        if not (port / name).is_file():
            raise RuntimeError('Missing build output: ' + name)
    if b'loginInfo.xml' in (port / 'client.js').read_bytes():
        raise RuntimeError('Build data with --no-private before making a preview')
    for name in ('manifest.bin', 'groups.txt'):
        if not (port / 'corpus' / name).is_file():
            raise RuntimeError('Missing corpus/' + name)
    destination.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='build-', dir=destination))
    try:
        # Copy engine/data: hard links could be overwritten by the next linker run.
        for name in PAGE_FILES + tuple(p.name for p in port.glob('client.locale_*')
                                       if PAGE.fullmatch('/' + p.name)):
            shutil.copy2(port / name, stage / name)
        page = (stage / 'client.html').read_text(encoding='utf-8')
        page, count = re.subn(
            r'(window\.m2w\s*=\s*\{\s*config:\s*\{\s*bridge:\s*)"[^"]*"',
            lambda m: m[1] + '"ws://127.0.0.1:%d"' % bridge_port, page)
        if count != 1:
            raise RuntimeError('Cannot set preview bridge in client.html')
        versions = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()[:24]
                    for p in stage.iterdir() if p.suffix in ('.js', '.wasm', '.data')}
        page = page.replace('var Module = {',
                            'var m2wDevVersions = ' + json.dumps(versions) + ';\nvar Module = {', 1)
        page, count = re.subn(
            r'locateFile:\s*function\s*\(p\)\s*\{\s*return\s+p\s*\+\s*"\?v=[^"]*";\s*\}',
            'locateFile: function (p) { return p + "?v=" + m2wDevVersions[p]; }', page)
        if count != 1:
            raise RuntimeError('Cannot version preview data/wasm URLs')
        page, count = re.subn(r's\.src\s*=\s*src\s*\+\s*"\?v=[^"]*";',
                              's.src = src + "?v=" + m2wDevVersions[src];', page)
        if count != 1:
            raise RuntimeError('Cannot version preview script URLs')
        page = re.sub(r'preload\.js\?v=[^"\s]+',
                      'preload.js?v=' + versions['preload.js'], page)
        (stage / 'client.html').write_text(page, encoding='utf-8')
        (stage / '.dev-versions.json').write_text(json.dumps(versions), encoding='utf-8')
        # The data package is tens of MB. Compress once, rather than send it raw
        # through the SSH tunnel on every reload.
        for asset in stage.iterdir():
            if asset.suffix in ('.js', '.wasm', '.data'):
                with asset.open('rb') as source, (stage / (asset.name + '.gz')).open('wb') as target:
                    with gzip.GzipFile(fileobj=target, mode='wb', compresslevel=1, mtime=0) as zipped:
                        shutil.copyfileobj(source, zipped)
        # /work in the build container is /home/m2web on the HTTP host.
        # Relative links survive that mount-prefix change.
        (stage / 'corpus').symlink_to(os.path.relpath((port / 'corpus').resolve(), stage.resolve()),
                                    target_is_directory=True)
        current = destination / 'current'
        previous = current.resolve() if current.is_symlink() else None
        temporary = destination / 'current.next'
        temporary.unlink(missing_ok=True)
        temporary.symlink_to(stage.name, target_is_directory=True)
        temporary.replace(current)
        # Keep one previous snapshot for in-flight requests and quick inspection.
        for old in destination.glob('build-*'):
            if old not in (stage, previous):
                shutil.rmtree(old)
        print('PREVIEW READY: engine/data copied; corpus reused; no CDN upload')
    except BaseException:
        if not (destination / 'current').is_symlink() or (destination / 'current').resolve() != stage:
            shutil.rmtree(stage)
        raise


def bridge_config_file(destination, page_port, bridge_port):
    import bridge_config
    source = ipaddress.ip_address(os.environ.get('M2W_DEV_CLIENT_IP', ''))
    if source.version != 4 or not source.is_global:
        raise RuntimeError('M2W_DEV_CLIENT_IP must be the public IPv4 address of the SSH peer')
    config = bridge_config.build_config(page_port=page_port)
    config.update(listenHost='127.0.0.1', listenPort=bridge_port,
                  allowedOrigins=['http://127.0.0.1:%d' % page_port,
                                  'http://localhost:%d' % page_port],
                  trustedProxies=[], trustProxy=False, devClientAddress=str(source))
    if not config['targets']:
        raise RuntimeError('No game-server targets configured')
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(config, indent=2), encoding='utf-8')
    # Contains only target addresses/settings; the unprivileged bridge must read it.
    destination.chmod(0o644)
    print('DEV BRIDGE: loopback only; %d targets; PROXY protocol=%s'
          % (len(config['targets']), config['proxyProtocol']))


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.wasm': 'application/wasm', '.js': 'text/javascript'}

    def end_headers(self):
        self.send_header('Cache-Control', 'public, max-age=31536000, immutable'
                         if getattr(self, 'asset_immutable', False) else 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def send_head(self):
        self.asset_immutable = False
        query = parse_qs(urlsplit(self.path).query)
        route = unquote(urlsplit(self.path).path)
        if route == '/__dev_health':
            import io
            body = b'{"preview":true}\n'
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            return io.BytesIO(body)
        if route == '/sw.js':
            import io
            body = (b"self.addEventListener('install',()=>self.skipWaiting());"
                    b"self.addEventListener('activate',e=>e.waitUntil(self.registration.unregister()));")
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            return io.BytesIO(body)
        if route == '/':
            route = '/client.html'
        if not (PAGE.fullmatch(route) or CORPUS.fullmatch(route)):
            self.send_error(404)
            return None
        # Pin the snapshot for this request even if a build switches current.
        self.directory = str(Path(self.directory).resolve())
        version = query.get('v', [None])[0]
        if version and PAGE.fullmatch(route) and route != '/client.html':
            versions = json.loads((Path(self.directory) / '.dev-versions.json').read_text())
            if versions.get(route[1:]) != version:
                self.send_error(409, 'Preview changed; reload client.html')
                return None
            self.asset_immutable = True
        if re.fullmatch(r'/corpus/[a-f0-9]{32}\.bin', route):
            self.asset_immutable = True
        self.path = route
        for encoding in self.headers.get('Accept-Encoding', '').lower().split(','):
            name, *parameters = [p.strip() for p in encoding.split(';')]
            if name != 'gzip':
                continue
            try:
                quality = next((float(p.partition('=')[2]) for p in parameters if p.startswith('q=')), 1)
            except ValueError:
                quality = 0
            zipped = Path(self.translate_path(route) + '.gz')
            if quality > 0 and PAGE.fullmatch(route) and zipped.is_file():
                source = zipped.open('rb')
                self.send_response(200)
                self.send_header('Content-Type', self.guess_type(route))
                self.send_header('Content-Encoding', 'gzip')
                self.send_header('Vary', 'Accept-Encoding')
                self.send_header('Content-Length', str(zipped.stat().st_size))
                self.end_headers()
                return source
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404)
        return None

    def log_request(self, code='-', size='-'):
        if str(code) != '200':
            super().log_request(code, size)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('snapshot', 'config', 'serve'))
    parser.add_argument('--root', required=True)
    parser.add_argument('--port', type=int, default=18731)
    parser.add_argument('--bridge-port', type=int, default=18732)
    parser.add_argument('--build-root')
    args = parser.parse_args()
    if args.action == 'snapshot':
        if not args.build_root:
            parser.error('snapshot requires --build-root')
        snapshot(args.build_root, args.root, args.bridge_port)
    elif args.action == 'config':
        bridge_config_file(args.root, args.port, args.bridge_port)
    else:
        handler = functools.partial(PreviewHandler, directory=args.root)
        with http.server.ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
            print('Preview listening on 127.0.0.1:%d' % args.port, flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
