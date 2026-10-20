import functools
import gzip
import http.client
import http.server
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from dev_preview import PAGE_FILES, PreviewHandler, snapshot, bridge_config_file


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='m2-preview-test-')
        self.root = Path(self.temp.name)
        self.build = self.root / 'port'
        self.build.mkdir()
        for name in PAGE_FILES:
            (self.build / name).write_text('test')
        (self.build / 'client.html').write_text(
            'window.m2w = { config: { bridge: "" } };\n'
            'var Module = { locateFile: function (p) { return p + "?v=1"; } };\n'
            's.src = src + "?v=1";\n<script src="preload.js?v=1"></script>')
        (self.build / 'corpus').mkdir()
        for name in ('manifest.bin', 'groups.txt', 'a' * 32 + '.bin'):
            (self.build / 'corpus' / name).write_bytes(b'corpus')
        self.destination = self.root / 'preview'

    def tearDown(self):
        self.temp.cleanup()

    def test_snapshot_is_independent_and_failure_preserves_previous(self):
        snapshot(self.build, self.destination, 18732)
        previous = (self.destination / 'current').resolve()
        self.assertFalse((previous / 'corpus').readlink().is_absolute())
        self.assertIn('ws://127.0.0.1:18732', (previous / 'client.html').read_text())
        (self.build / 'client.wasm').write_text('new-build')
        self.assertEqual((previous / 'client.wasm').read_text(), 'test')
        (self.build / 'client.js').write_text('loginInfo.xml')
        with self.assertRaises(RuntimeError):
            snapshot(self.build, self.destination, 18732)
        self.assertEqual((self.destination / 'current').resolve(), previous)

    def test_bridge_uses_only_the_public_ssh_peer(self):
        import sys
        module = SimpleNamespace(build_config=lambda **kwargs: {
            'targets': {'auth': {'host': '192.168.122.10', 'port': 30001}},
            'proxyProtocol': True})
        output = self.root / 'bridge.json'
        with patch.dict(sys.modules, bridge_config=module):
            with patch.dict(os.environ, M2W_DEV_CLIENT_IP='8.8.8.8'):
                bridge_config_file(output, 18731, 18732)
            config = json.loads(output.read_text())
            self.assertEqual(config['devClientAddress'], '8.8.8.8')
            self.assertEqual(config['listenHost'], '127.0.0.1')
            self.assertTrue(config['proxyProtocol'])
            self.assertFalse(config['trustProxy'])
            with patch.dict(os.environ, M2W_DEV_CLIENT_IP='127.0.0.1'):
                with self.assertRaises(RuntimeError):
                    bridge_config_file(output, 18731, 18732)

    def test_server_allows_only_assets_and_disables_cache(self):
        snapshot(self.build, self.destination, 18732)
        current = self.destination / 'current'
        (current / 'secret.txt').write_text('never serve')
        handler = functools.partial(PreviewHandler, directory=str(current))
        with http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                connection = http.client.HTTPConnection('127.0.0.1', server.server_port)
                for route in ('/client.html?v=1', '/client.wasm', '/corpus/' + 'a' * 32 + '.bin'):
                    connection.request('GET', route)
                    response = connection.getresponse()
                    self.assertEqual(response.status, 200, route)
                    expected = 'public, max-age=31536000, immutable' if '/corpus/' in route else 'no-store'
                    self.assertEqual(response.getheader('Cache-Control'), expected)
                    response.read()
                for route in ('/secret.txt', '/private/loginInfo.xml', '/corpus/',
                              '/%2e%2e/secret.txt', '/corpus/../secret.txt'):
                    connection.request('GET', route)
                    response = connection.getresponse()
                    self.assertEqual(response.status, 404, route)
                    response.read()
                connection.request('GET', '/sw.js')
                response = connection.getresponse()
                self.assertIn(b'unregister', response.read())
                connection.request('GET', '/client.wasm', headers={'Accept-Encoding': 'gzip'})
                response = connection.getresponse()
                self.assertEqual(response.getheader('Content-Encoding'), 'gzip')
                self.assertEqual(gzip.decompress(response.read()), b'test')
                connection.request('GET', '/client.wasm', headers={'Accept-Encoding': 'gzip;q=0'})
                response = connection.getresponse()
                self.assertIsNone(response.getheader('Content-Encoding'))
                self.assertEqual(response.read(), b'test')
                versions = json.loads((current / '.dev-versions.json').read_text())
                connection.request('GET', '/client.data?v=' + versions['client.data'])
                response = connection.getresponse()
                self.assertEqual(response.status, 200)
                self.assertIn('immutable', response.getheader('Cache-Control'))
                response.read()
                connection.request('GET', '/client.data?v=old-build')
                response = connection.getresponse()
                self.assertEqual(response.status, 409)
                self.assertEqual(response.getheader('Cache-Control'), 'no-store')
                response.read()
                connection.close()
            finally:
                server.shutdown()
                thread.join()


if __name__ == '__main__':
    unittest.main()
