'use strict';
// node --test tools/generate-ids.test.js
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { generateId, resolveType, sanitizeSlug, saoPauloStamp } = require('./generate-ids.js');

const T = Date.UTC(2026, 8, 26, 3, 50, 28); // 00:50:28 in Sao Paulo (UTC-3)

test('format and Sao Paulo clock', () => {
  assert.equal(saoPauloStamp(T), '20260926-005028');
  assert.equal(generateId('prompt', 'Fix login timeout', { nowMs: T }), 'WORION-PROMPT-20260926-005028-fix-login-timeout');
});

test('every type and the aliases resolve', () => {
  for (const t of ['command', 'prompt', 'execution', 'response', 'artifact', 'event', 'ponte', 'blueprint', 'review', 'entry']) {
    assert.match(generateId(t, 'x', { nowMs: T }), /^WORION-[A-Z]+-20260926-005028-x$/);
  }
  assert.equal(resolveType('exec'), 'execution');
  assert.throws(() => resolveType('job'), /unknown type/);
});

test('slug: accents removed, lowercase, hyphens, 40 chars max, never empty', () => {
  assert.equal(sanitizeSlug('Revisão da Governança!'), 'revisao-da-governanca');
  assert.ok(sanitizeSlug('a'.repeat(80)).length <= 40);
  assert.throws(() => sanitizeSlug('---'), /empty/);
});

test('an ID already in the repository is not reused', t => {
  const repo = fs.mkdtempSync(path.join(os.tmpdir(), 'ids-'));
  t.after(() => fs.rmSync(repo, { recursive: true, force: true }));
  const git = (...a) => spawnSync('git', ['-C', repo, '-c', 'user.name=t', '-c', 'user.email=t@t', ...a], { encoding: 'utf8' });
  git('init', '-q');
  const taken = generateId('prompt', 'same cause', { nowMs: T });
  fs.writeFileSync(path.join(repo, 'bridge.md'), `${taken}\n`);
  git('add', 'bridge.md');
  git('commit', '-q', '-m', 'x');
  const next = generateId('prompt', 'same cause', { nowMs: T, repo });
  assert.notEqual(next, taken);
  assert.equal(next, 'WORION-PROMPT-20260926-005029-same-cause');
});
