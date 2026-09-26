#!/usr/bin/env node
'use strict';
/**
 * generate-ids — one canonical generator for every identifier in the causal chain.
 *
 *   node tools/generate-ids.js <type> <purpose> [--repo <dir>]
 *   node tools/generate-ids.js prompt fix-login-timeout
 *   -> WORION-PROMPT-20260926-005028-fix-login-timeout
 *
 * Format: <PREFIX>-<YYYYMMDD>-<HHMMSS>-<slug>, clock America/Sao_Paulo, slug lowercase ASCII with hyphens
 * (accents removed, max 40 chars). IDs are generated, never typed: a typed ID once collided with another
 * executor's. With --repo, an ID already present in that Git repository is never reused; the generator waits
 * for the next second instead.
 *
 * Who generates which ID is in docs/continuity/ID_GENERATORS.md. The Notion <-> GitHub publication pair
 * has its own generator: tools/generate-publication-ids.js.
 */
const { spawnSync } = require('node:child_process');

const TYPES = {
  command: 'WORION-CMD',          // an order, when the flow tracks it separately from the prompt
  prompt: 'WORION-PROMPT',        // the cause: the prompt (or a direct order from the human)
  execution: 'WORION-EXEC',       // one run of one executor
  response: 'WORION-RESP',        // the executor's reply
  artifact: 'WORION-ART',         // a produced artifact
  event: 'WORION-EVT',            // an event, e.g. a mailbox message
  ponte: 'WORION-PONTE',          // the daily bridge
  blueprint: 'WORION-BLUEPRINT',  // the job's persistent record
  review: 'WORION-REVIEW',        // a request for the governor's attestation
  entry: 'WORION-ENTRY',          // a file the human delivered
};
const ALIASES = { cmd: 'command', exec: 'execution', resp: 'response', art: 'artifact', evt: 'event', entrega: 'entry' };

function resolveType(raw) {
  const t = String(raw || '').toLowerCase();
  const type = TYPES[t] ? t : ALIASES[t];
  if (!type) throw new Error(`unknown type "${raw}"; use one of: ${Object.keys(TYPES).join(', ')}`);
  return type;
}

function sanitizeSlug(raw) {
  const slug = String(raw || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40).replace(/-+$/g, '');
  if (!slug) throw new Error('empty purpose');
  return slug;
}

function saoPauloStamp(nowMs) {
  const parts = Object.fromEntries(new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23',
  }).formatToParts(new Date(nowMs)).map(p => [p.type, p.value]));
  return `${parts.year}${parts.month}${parts.day}-${parts.hour}${parts.minute}${parts.second}`;
}

function existsInRepo(repo, id) {
  const r = spawnSync('git', ['-C', repo, 'grep', '-q', '-F', id], { encoding: 'utf8' });
  return r.status === 0;
}

function generateId(typeRaw, purpose, { nowMs = Date.now(), repo = null } = {}) {
  const prefix = TYPES[resolveType(typeRaw)];
  const slug = sanitizeSlug(purpose);
  for (let i = 0; i < 60; i += 1) {
    const id = `${prefix}-${saoPauloStamp(nowMs + i * 1000)}-${slug}`;
    if (!repo || !existsInRepo(repo, id)) return id;
  }
  throw new Error('no free ID in the next 60 seconds');
}

if (require.main === module) {
  try {
    const args = process.argv.slice(2);
    const r = args.indexOf('--repo');
    const repo = r >= 0 ? args.splice(r, 2)[1] : null;
    const [type, ...words] = args;
    process.stdout.write(`${generateId(type, words.join(' '), { repo })}\n`);
  } catch (e) {
    process.stderr.write(`${e.message}\n`);
    process.exit(2);
  }
}

module.exports = { TYPES, generateId, resolveType, sanitizeSlug, saoPauloStamp };
