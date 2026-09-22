#!/usr/bin/env node
'use strict';

/**
 * @file Gerador canonico e universal de IDs do Worion.
 * @contract WORION-PROMPT-ID-GEN-001
 * @status active
 * @provenance IA EXECUTORA: DeepSeek V4 (harness Claude Code)
 * @provenance RESPONSE_TO_PROMPT_ID: GPTSOL-DEEPSEEK-RECONSTRUCAO-START-20260823-1000
 * @provenance AUTORIA INTELECTUAL: Glaydson (doc/03 §0 + cadeia de IDs do contrato vigente)
 *
 * Cadeia vigente (contracts/PROMPT_EXECUTION_PROVENANCE_CONTRACT.md):
 *
 *   COMMAND_ID → PROMPT_ID → EXECUTION_ID → RESPONSE_ID → ARTIFACT_ID / EVENT_ID → commit/resultado
 *
 * Formatos canonicos (mesmo contrato):
 *
 *   WORION-CMD-AAAAMMDD-HHMMSS-<slug-curto>     (command)
 *   WORION-PROMPT-AAAAMMDD-HHMMSS-<slug-curto>  (prompt)
 *   WORION-EXEC-AAAAMMDD-HHMMSS-<slug-curto>    (execution)
 *   WORION-RESP-AAAAMMDD-HHMMSS-<slug-curto>    (response)
 *   WORION-ART-AAAAMMDD-HHMMSS-<slug-curto>     (artifact)
 *   WORION-EVT-AAAAMMDD-HHMMSS-<slug-curto>     (event)
 *
 * Regras:
 * - horario real de America/Sao_Paulo;
 * - slug curto de finalidade, sanitizado (minusculas, sem acento, hifens);
 * - determinista quanto ao formato, unico quanto ao valor;
 * - nao reutiliza ID ja existente no repositorio (confere com git grep);
 * - zero modelo, zero rede;
 * - chamavel por Claude Code, Codex, DeepSeek ou qualquer executor.
 *
 * Uso CLI (compativel com a versao anterior + interface universal):
 *   node scripts/generate-prompt-id.js <slug>                 # tipo default: prompt
 *   node scripts/generate-prompt-id.js <tipo> <slug>          # command|prompt|execution|response|artifact|event
 *   node scripts/generate-prompt-id.js prompt "reconstrucao-linha-do-tempo"
 *
 * Uso programatico (testavel):
 *   const { generatePromptId, generateWorionId, TYPES } = require('./scripts/generate-prompt-id.js');
 *   generatePromptId('meu-slug');                        // prompt, agora, America/Sao_Paulo
 *   generatePromptId('meu-slug', { nowMs });             // tempo fixo para teste
 *   generateWorionId('artifact', 'linha-do-tempo', { nowMs });
 */

const { spawnSync } = require('node:child_process');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');

// Tipos canonicos da cadeia de IDs (contrato vigente).
const TYPES = {
  command: 'WORION-CMD',
  prompt: 'WORION-PROMPT',
  execution: 'WORION-EXEC',
  response: 'WORION-RESP',
  artifact: 'WORION-ART',
  event: 'WORION-EVT',
};
const TYPE_ALIASES = {
  cmd: 'command',
  exec: 'execution',
  resp: 'response',
  art: 'artifact',
  evt: 'event',
  event: 'event',
  artifact: 'artifact',
  response: 'response',
  execution: 'execution',
  command: 'command',
  prompt: 'prompt',
};
const FORMAT_PREFIX = TYPES.prompt;

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
  const parts = Object.fromEntries(fmt.formatToParts(new Date(nowMs)).map((p) => [p.type, p.value]));
  return {
    date: `${parts.year}${parts.month}${parts.day}`,
    time: `${parts.hour}${parts.minute}${parts.second}`,
  };
}

function sanitizeSlug(raw) {
  const base = String(raw || '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 40);
  if (!base) {
    throw new Error('slug vazio apos sanitizacao: informe finalidade curta, ex. "linha-do-tempo"');
  }
  return base;
}

function existsInRepo(id) {
  // Somente-leitura: consulta git sem tocar working tree. Se o git falhar por
  // qualquer motivo (repo, caminho), assume inexistente e segue — o colapso
  // aqui nao pode impedir a geracao; a unicidade real vem do timestamp+slug.
  const result = spawnSync('git', ['grep', '-l', '--', id], {
    cwd: ROOT,
    encoding: 'utf8',
    windowsHide: true,
    timeout: 15000,
  });
  if (result.error || result.status === null) return false;
  const lines = String(result.stdout || '').split(/\r?\n/).filter(Boolean);
  return lines.length > 0;
}

function resolveType(raw) {
  const key = String(raw || 'prompt').toLowerCase().trim();
  return TYPE_ALIASES[key] || (TYPES[key] ? key : null);
}

function generateWorionId(rawType, rawSlug, options = {}) {
  const type = resolveType(rawType);
  if (!type) {
    throw new Error(
      `tipo desconhecido: "${rawType}". Tipos canonicos: command|prompt|execution|response|artifact|event`
    );
  }
  const nowMs = Number.isFinite(options.nowMs) ? options.nowMs : Date.now();
  const slug = sanitizeSlug(rawSlug);
  const { date, time } = saoPauloParts(nowMs);
  const base = `${TYPES[type]}-${date}-${time}-${slug}`;
  let id = base;
  let n = 2;
  while (existsInRepo(id) && n <= 999) {
    id = `${base}-${n}`;
    n += 1;
  }
  return id;
}

function generatePromptId(rawSlug, options = {}) {
  return generateWorionId('prompt', rawSlug, options);
}

module.exports = {
  generatePromptId,
  generateWorionId,
  resolveType,
  sanitizeSlug,
  saoPauloParts,
  FORMAT_PREFIX,
  TYPES,
};

if (require.main === module) {
  const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  // Forma 1 (legado): <slug> — tipo prompt.
  // Forma 2 (universal): <tipo> <slug>.
  let type = 'prompt';
  let slug = '';
  if (args.length === 1) {
    slug = args[0];
  } else if (args.length >= 2) {
    type = args[0];
    slug = args[1];
  } else {
    slug = '';
  }
  try {
    process.stdout.write(generateWorionId(type, slug) + '\n');
  } catch (error) {
    process.stderr.write(`[generate-prompt-id] ${error.message}\n`);
    process.exitCode = 1;
  }
}
