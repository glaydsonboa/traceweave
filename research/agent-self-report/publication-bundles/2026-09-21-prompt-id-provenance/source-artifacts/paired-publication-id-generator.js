#!/usr/bin/env node
'use strict';

function saoPauloParts(nowMs) {
  const fmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Sao_Paulo',
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,
  });
  const parts = Object.fromEntries(fmt.formatToParts(new Date(nowMs)).map(p => [p.type, p.value]));
  return { date: `${parts.year}${parts.month}${parts.day}`, time: `${parts.hour}${parts.minute}${parts.second}` };
}
function sanitizeSlug(raw) {
  const slug = String(raw || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40);
  if (!slug) throw new Error('empty slug');
  return slug;
}
function generatePair(slugRaw, nowMs = Date.now()) {
  const {date,time} = saoPauloParts(nowMs);
  const key = `${date}-${time}-${sanitizeSlug(slugRaw)}`;
  return { pair_key:key, notion_id:`PROV-NOTION-${key}`, github_id:`PROV-GITHUB-${key}`, generated_at_timezone:'America/Sao_Paulo' };
}
if (require.main === module) {
  const slug = process.argv[2] || '';
  const p = generatePair(slug);
  process.stdout.write(`NOTION_ID=${p.notion_id}\nGITHUB_ID=${p.github_id}\nPAIR_KEY=${p.pair_key}\n`);
}
module.exports={generatePair,sanitizeSlug,saoPauloParts};
