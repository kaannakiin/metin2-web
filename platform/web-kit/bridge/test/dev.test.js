'use strict';

const assert = require('node:assert/strict');
const net = require('node:net');
const { test } = require('node:test');
const { WebSocket } = require('ws');
const { tunnelAddress } = require('../src/dev.js');
const { loadConfig } = require('../src/config.js');
const { createProxyServer } = require('../src/server.js');

test('tunnel address requires loopback binding, localhost origins and a public IPv4', () => {
  const config = { listenHost: '127.0.0.1', devClientAddress: '8.8.8.8',
    allowedOrigins: ['http://127.0.0.1:18731'] };
  assert.equal(tunnelAddress(config), '8.8.8.8');
  for (const address of ['127.0.0.1', '192.168.1.1', '10.0.0.1', '::1', 'invalid']) {
    assert.throws(() => tunnelAddress({ ...config, devClientAddress: address }));
  }
  assert.throws(() => tunnelAddress({ ...config, listenHost: '0.0.0.0' }));
  assert.throws(() => tunnelAddress({ ...config, allowedOrigins: [] }));
  assert.throws(() => tunnelAddress({ ...config, allowedOrigins: ['https://example.com'] }));
});

for (const override of [false, true]) {
  test(`PROXY source uses ${override ? 'the SSH peer' : 'the default socket peer'}`, { timeout: 5000 }, async () => {
    const sockets = new Set();
    let resolveHeader;
    const header = new Promise((resolve) => { resolveHeader = resolve; });
    const upstream = net.createServer((socket) => {
      sockets.add(socket);
      socket.once('close', () => sockets.delete(socket));
      let buffer = '';
      socket.on('data', (data) => {
        buffer += data.toString();
        if (buffer.includes('\r\n')) resolveHeader(buffer.split('\r\n')[0]);
      });
    });
    await new Promise((resolve) => upstream.listen(0, '127.0.0.1', resolve));
    const config = loadConfig({ listenHost: '127.0.0.1', listenPort: 0,
      proxyProtocol: true, trustProxy: false, heartbeatMs: 0,
      allowedOrigins: ['http://127.0.0.1:18731'],
      targets: { auth: { host: '127.0.0.1', port: upstream.address().port } } });
    const proxy = createProxyServer(config, override ? { addressOf: () => '8.8.8.8' } : {});
    let ws;
    try {
      const { port } = await proxy.listen();
      ws = new WebSocket(`ws://127.0.0.1:${port}/?target=auth`, {
        origin: 'http://127.0.0.1:18731',
        headers: { 'X-Forwarded-For': '1.1.1.1', 'CF-Connecting-IP': '1.1.1.1' },
      });
      await new Promise((resolve, reject) => { ws.once('open', resolve); ws.once('error', reject); });
      assert.equal(await header,
        `PROXY TCP4 ${override ? '8.8.8.8' : '127.0.0.1'} 127.0.0.1 0 ${upstream.address().port}`);
    } finally {
      if (ws) ws.terminate();
      await proxy.close();
      for (const socket of sockets) socket.destroy();
      await new Promise((resolve) => upstream.close(resolve));
    }
  });
}
