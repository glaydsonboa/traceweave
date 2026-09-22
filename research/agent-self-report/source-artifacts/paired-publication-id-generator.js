#!/usr/bin/env node
'use strict';

/**
 * Worion — gerador de IDs para atualização material externa.
 *
 * Gera, como um par atômico:
 *   - NOTION_ID
 *   - GITHUB_ID
 *
 * Os IDs identificam a atualização/materialização atual. Eles NÃO provam
 * publicação por si sós. A prova exige os IDs nativos do destino + readback.
 *
 * Exemplo:
 *   node generate-update-ids.js "publicar-transcript-traceweave"
 *
 * Saída:
 *   NOTION_ID=WORION-NOTION-AAAAMMDD-HHMMSS-<slug>
 *   GITHUB_ID=WORION-GITHUB-AAAAMMDD-HHMMSS-<slug>
 *   PAIR_KEY=AAAAMMDD-HHMMSS-<slug>
 *
 * JSON:
 *   node generate-update-ids.js "publicar-transcript-traceweave" --json
 */

const { spawnSync } = require('node:child_process');

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
    fmt.formatToParts(new Date(nowMs)).map((x) => [x.type, x.value]),
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
    throw new Error('slug vazio apos sanitizacao');
  }

  return slug;
}

function existsInRepo(root, id) {
  const result = spawnSync('git', ['grep', '-l', '--', id], {
    cwd: root,
    encoding: 'utf8',
    windowsHide: true,
    timeout: 15000,
  });

  if (result.error || result.status === null) return false;
  return String(result.stdout || '').trim().length > 0;
}

function generatePair(slugRaw, options = {}) {
  const nowMs = Number.isFinite(options.nowMs) ? options.nowMs : Date.now();
  const root = options.root || process.cwd();
  const slug = sanitizeSlug(slugRaw);
  const { date, time } = saoPauloParts(nowMs);

  const keyBase = `${date}-${time}-${slug}`;
  let key = keyBase;
  let suffix = 2;

  while (
    (
      existsInRepo(root, `WORION-NOTION-${key}`) ||
      existsInRepo(root, `WORION-GITHUB-${key}`)
    ) &&
    suffix <= 999
  ) {
    key = `${keyBase}-${suffix}`;
    suffix += 1;
  }

  return {
    pair_key: key,
    notion_id: `WORION-NOTION-${key}`,
    github_id: `WORION-GITHUB-${key}`,
    generated_at_timezone: 'America/Sao_Paulo',
  };
}

module.exports = {
  generatePair,
  sanitizeSlug,
  saoPauloParts,
};

if (require.main === module) {
  const args = process.argv.slice(2);
  const json = args.includes('--json');
  const slug = args.find((a) => !a.startsWith('--')) || '';

  try {
    const pair = generatePair(slug);

    if (json) {
      process.stdout.write(`${JSON.stringify(pair)}\n`);
    } else {
      process.stdout.write(`NOTION_ID=${pair.notion_id}\n`);
      process.stdout.write(`GITHUB_ID=${pair.github_id}\n`);
      process.stdout.write(`PAIR_KEY=${pair.pair_key}\n`);
    }
  } catch (error) {
    process.stderr.write(`[generate-update-ids] ${error.message}\n`);
    process.exitCode = 1;
  }
}
