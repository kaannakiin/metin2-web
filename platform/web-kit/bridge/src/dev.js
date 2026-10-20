'use strict';

// Private SSH preview entry point. A tunnel hides the player's public address;
// use the SSH peer recorded by the host, never a browser-supplied header.
const fs = require('node:fs');
const { isIPv4 } = require('node:net');
const { loadConfig } = require('./config.js');
const { createProxyServer, isNonPublic } = require('./server.js');

function tunnelAddress(config) {
  if (!['127.0.0.1', '::1'].includes(config.listenHost)) {
    throw new Error('Development bridge must listen on loopback');
  }
  if (!isIPv4(config.devClientAddress) || isNonPublic(config.devClientAddress)) {
    throw new Error('Development bridge needs the public IPv4 address of the SSH peer');
  }
  if (!config.allowedOrigins?.length || config.allowedOrigins.some((origin) => {
    const url = new URL(origin);
    return !['http:', 'https:'].includes(url.protocol) ||
      !['localhost', '127.0.0.1', '[::1]'].includes(url.hostname);
  })) {
    throw new Error('Development bridge permits only explicit localhost origins');
  }
  return config.devClientAddress;
}

async function main() {
  const config = loadConfig(JSON.parse(fs.readFileSync(process.argv[2], 'utf8')));
  const address = tunnelAddress(config);
  const logger = (event, details = {}) => process.stdout.write(
    JSON.stringify({ ts: new Date().toISOString(), event, ...details }) + '\n');
  const server = createProxyServer(config, { logger, addressOf: () => address });
  const { port } = await server.listen();
  logger('listening', { host: config.listenHost, port });
  let stopping = false;
  const stop = async () => {
    if (stopping) return;
    stopping = true;
    await server.close();
    process.exit(0);
  };
  process.once('SIGINT', stop);
  process.once('SIGTERM', stop);
}

if (require.main === module) {
  main().catch((error) => {
    process.stderr.write(error.message + '\n');
    process.exit(1);
  });
}

module.exports = { tunnelAddress };
