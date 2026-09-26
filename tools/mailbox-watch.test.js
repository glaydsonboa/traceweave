'use strict';
// node --test tools/mailbox-watch.test.js
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { news } = require('./mailbox-watch.js');

function box(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'mailbox-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, 'deepseek', 'new'), { recursive: true });
  fs.mkdirSync(path.join(root, 'deepseek', 'cur'), { recursive: true });
  return root;
}
function send(root, id, subject) {
  fs.writeFileSync(path.join(root, 'deepseek', 'new', `${id}.json`),
    JSON.stringify({ id, from: 'claude', to: 'deepseek', subject, created_at: new Date().toISOString() }));
}
function ack(root, id) {
  fs.renameSync(path.join(root, 'deepseek', 'new', `${id}.json`), path.join(root, 'deepseek', 'cur', `${id}.json`));
}

test('a message already waiting when the watcher starts is reported on the first pass', t => {
  const root = box(t);
  send(root, 'm1', 'REVIEW waiting before the watcher');
  const lines = news(root, 'deepseek', new Set());
  assert.deepEqual(lines, ['MAILBOX m1 · claude -> deepseek · REVIEW waiting before the watcher']);
});

test('each message is reported once; a new one on the next pass', t => {
  const root = box(t);
  const seen = new Set();
  send(root, 'm1', 'first');
  assert.equal(news(root, 'deepseek', seen).length, 1);
  assert.equal(news(root, 'deepseek', seen).length, 0);
  send(root, 'm2', 'second');
  assert.deepEqual(news(root, 'deepseek', seen), ['MAILBOX m2 · claude -> deepseek · second']);
});

test('an inbox emptied by an acknowledgement prints nothing', t => {
  const root = box(t);
  const seen = new Set();
  send(root, 'm1', 'to acknowledge');
  news(root, 'deepseek', seen);
  ack(root, 'm1');
  assert.deepEqual(news(root, 'deepseek', seen), []);
});
