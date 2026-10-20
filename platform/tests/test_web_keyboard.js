const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function keyboard() {
    const source = fs.readFileSync(path.join(__dirname, '../web-kit/compat/runtime.js'), 'utf8');
    const start = source.indexOf('m2w.dikStart = function ()');
    const end = source.indexOf('// Language and font', start);
    const listeners = {};
    const context = {
        m2w: {},
        document: { addEventListener: (name, fn) => { listeners[name] = fn; } },
        addEventListener: (name, fn) => { listeners[name] = fn; },
    };
    vm.runInNewContext(source.slice(start, end), context);
    context.m2w.dikStart();
    function event(type, code, key) {
        let prevented = false;
        listeners[type]({ code, key, preventDefault() { prevented = true; } });
        return prevented;
    }
    return { state: context.m2w.dik, event, blur: () => listeners.blur() };
}

test('Turkish quote pickup survives modifier release and repeat', () => {
    const { state, event } = keyboard();
    assert.equal(event('keydown', 'Digit2', '"'), true);
    assert.equal(state[41], 1);
    assert.equal(state[3], 0);
    event('keydown', 'Digit2', '2');
    assert.equal(state[41], 1);
    assert.equal(state[3], 0);
    event('keyup', 'Digit2', '2');
    assert.equal(state[41], 0);
    event('keydown', 'Digit2', '2');
    assert.equal(state[3], 1);
});

test('pickup aliases release independently; blur releases attack and pickup', () => {
    const { state, event, blur } = keyboard();
    event('keydown', 'Backquote', '`');
    event('keydown', 'Quote', '"');
    event('keyup', 'Backquote', '`');
    assert.equal(state[41], 1);
    event('keydown', 'Space', ' ');
    assert.equal(state[57], 1);
    blur();
    assert.equal(state.some(Boolean), false);
    event('keyup', 'Quote', "'");
    event('keydown', 'Space', ' ');
    event('keyup', 'Space', ' ');
    assert.equal(state[57], 0);
});

test('Z pickup, ordinary quote and browser-owned shortcuts retain bindings', () => {
    const { state, event } = keyboard();
    event('keydown', 'KeyZ', 'z');
    assert.equal(state[44], 1);
    event('keydown', 'Quote', "'");
    assert.equal(state[40], 1);
    assert.equal(state[41], 0);
    assert.equal(event('keydown', 'F5', 'F5'), false);
    assert.equal(event('keydown', 'F12', 'F12'), false);
});
