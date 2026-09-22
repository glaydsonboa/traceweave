#!/usr/bin/env node
'use strict';

/**
 * Neutral provenance identity-chain generator.
 *
 * Public derivative of a historical source artifact. The historical source
 * identity is preserved in the provenance record; this file intentionally
 * removes system-specific names and contract references.
 *
 * Chain:
 *   COMMAND_ID → PROMPT_ID → EXECUTION_ID → RESPONSE_ID → ARTIFACT_ID / EVENT_ID
 *
 * Formats:
 *   PROV-CMD-AAAAMMDD-HHMMSS-<slug>     (command)
 *   PROV-PROMPT-AAAAMMDD-HHMMSS-<slug>  (prompt)
 *   PROV-EXEC-AAAAMMDD-HHMMSS-<slug>    (execution)
 *   PROV-RESP-AAAAMMDD-HHMMSS-<slug>    (response)
 *   PROV-ART-AAAAMMDD-HHMMSS-<slug>     (artifact)
 *   PROV-EVT-AAAAMMDD-HHMMSS-<slug>     (event)
 *
 * Properties:
 * - deterministic format;
 * - America/Sao_Paulo timestamp, preserving source behavior;
 * - sanitized purpose slug;
 * - zero model and zero network;
 * - collision check against the current Git repository when available.
 *
 * CLI:
 *   node identity-chain-generator.js <slug>                 # prompt
 *   node identity-chain-generator.js <type> <slug>          # explicit type
 */

const { spawnSync } = require('node:child_process');
const path = require('node:path');

const TYPES = Object.freeze({
  command: 'PROV-CMD',
  prompt: 'PROV-PROMPT',
  execution: 'PROV-EXEC',
  response: 'PROV-RESP',
  artifact: 'PROV-ART',
  event: 'PROV-EVT',
});

const TYPE_ALIASES = Object.freeze({
  cmd: 'command',
  exec: 'execution',
  resp: 'response',
  art: 'artifact',
  evt: 'event',
  command: 'command',
  prompt: 'prompt',
  execution: 'execution',
  response: 'response',
  artifact: 'artifact',
  event: 'event',
});

function resolveRepositoryRoot(startDir = __dirname) {
  const result = spawnSync('git', ['rev-parse', '--show-toplevel'], {
    cwd: startDir,
    encoding: 'utf8',
    windowsHide: true,
    timeout: 15000,
  });
  if (!result.error && result.status === 0) {
    const root = String(result.stdout || '').trim();
    if (root) return path.resolve(root);
  }
  return path.resolve(process.cwd());
}

function saoPauloParts(nowMs) {
  const fmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Sao_Paulo',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
  const parts = Object.fromEntries(
    fmt.formatToParts(new Date(nowMs)).map((part) => [part.type, part.value]),
  );
  return {
    date: `${parts.year}${parts.month}${parts.day}`,
    time: `${parts.hour}${parts.minute}${parts.second}`,
  };
}

function sanitizeSlug(raw) {
  const slug = String(raw || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 40);

  if (!slug) {
    throw new Error('empty slug after sanitization');
  }
  return slug;
}

function resolveType(raw) {
  const key = String(raw || 'prompt').toLowerCase().trim();
  return TYPE_ALIASES[key] || null;
}

function existsInRepo(repoRoot, id) {
  const result = spawnSync('git', ['grep', '-l', '--', id], {
    cwd: repoRoot,
    encoding: 'utf8',
    windowsHide: true,
    timeout: 15000,
  });
  if (result.error || result.status === null) return false;
  return String(result.stdout || '').trim().length > 0;
}

function generateId(rawType, rawSlug, options = {}) {
  const type = resolveType(rawType);
  if (!type) {
    throw new Error(
      `unknown type: "${rawType}". Expected command|prompt|execution|response|artifact|event`,
    );
  }

  const nowMs = Number.isFinite(options.nowMs) ? options.nowMs : Date.now();
  const repoRoot = options.repoRoot || resolveRepositoryRoot(options.startDir || __dirname);
  const slug = sanitizeSlug(rawSlug);
  const { date, time } = saoPauloParts(nowMs);
  const base = `${TYPES[type]}-${date}-${time}-${slug}`;

  let id = base;
  let suffix = 2;
  while (existsInRepo(repoRoot, id) && suffix <= 999) {
    id = `${base}-${suffix}`;
    suffix += 1;
  }
  return id;
}

function generatePromptId(rawSlug, options = {}) {
  return generateId('prompt', rawSlug, options);
}

module.exports = {
  TYPES,
  generateId,
  generatePromptId,
  resolveRepositoryRoot,
  resolveType,
  sanitizeSlug,
  saoPauloParts,
};

if (require.main === module) {
  const args = process.argv.slice(2).filter((arg) => !arg.startsWith('--'));
  let type = 'prompt';
  let slug = '';

  if (args.length === 1) {
    slug = args[0];
  } else if (args.length >= 2) {
    [type, slug] = args;
  }

  try {
    process.stdout.write(`${generateId(type, slug)}\n`);
  } catch (error) {
    process.stderr.write(`[identity-chain-generator] ${error.message}\n`);
    process.exitCode = 1;
  }
}
