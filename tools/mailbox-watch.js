#!/usr/bin/env node
'use strict';
/**
 * mailbox-watch — wake an idle coding agent when a message lands in its mailbox.
 *
 * A mailbox is a directory per agent: <root>/<agent>/new/*.json. Each file is one message
 * ({ id, from, to, subject, created_at }). Another agent writes it atomically (tmp -> new) and the
 * receiver moves it out of new/ when it acknowledges it.
 *
 * This script prints ONE line per message waiting in new/: first every message already there when it
 * starts, then each new one as it arrives. Nothing else is printed, not even an empty line.
 *
 * Run it under a tool that turns each stdout line into an event for the agent — in Claude Code, the
 * Monitor tool — and an idle session wakes up when a request arrives, without a human relaying it.
 *
 *   node tools/mailbox-watch.js --root .mailbox --agent claude [--interval 5] [--once]
 *
 * Both rules below come from a first, hand-written watcher that failed in real use (25/09/2026):
 *   - it only reported files created AFTER it started, so two requests already waiting were never seen;
 *   - it printed an empty line whenever the inbox was emptied by an acknowledgement.
 */
const fs = require('node:fs');
const path = require('node:path');

function parseArgs(argv) {
  const args = { root: '.mailbox', agent: null, interval: 5, once: false };
  for (let i = 0; i < argv.length; i += 1) {
    const t = argv[i];
    if (t === '--root') args.root = argv[++i];
    else if (t === '--agent') args.agent = argv[++i];
    else if (t === '--interval') args.interval = Number(argv[++i]);
    else if (t === '--once') args.once = true;
    else throw new Error(`unexpected argument: ${t}`);
  }
  if (!args.agent) throw new Error('usage: mailbox-watch.js --root <dir> --agent <name>');
  if (!(args.interval > 0)) throw new Error('--interval must be > 0');
  return args;
}

function pending(root, agent) {
  const dir = path.join(root, agent, 'new');
  let names;
  try { names = fs.readdirSync(dir); } catch (e) { if (e.code === 'ENOENT') return []; throw e; }
  const out = [];
  for (const name of names.filter(n => n.endsWith('.json')).sort()) {
    try {
      const m = JSON.parse(fs.readFileSync(path.join(dir, name), 'utf8'));
      if (m && m.id) out.push(m);
    } catch { /* a file still being written is picked up on the next pass */ }
  }
  return out;
}

/** Lines for messages not reported yet. Mutates `seen`. */
function news(root, agent, seen) {
  const lines = [];
  for (const m of pending(root, agent)) {
    if (seen.has(m.id)) continue;
    seen.add(m.id);
    lines.push(`MAILBOX ${m.id} · ${m.from} -> ${m.to} · ${String(m.subject || '').replace(/\s+/g, ' ')}`);
  }
  return lines;
}

function watch({ root, agent, interval, once }, write = l => process.stdout.write(`${l}\n`)) {
  const seen = new Set();
  const pass = () => {
    try { for (const l of news(root, agent, seen)) write(l); }
    catch (e) { process.stderr.write(`mailbox-watch: ${e.message}\n`); }
  };
  pass();
  return once ? null : setInterval(pass, interval * 1000);
}

if (require.main === module) {
  try { watch(parseArgs(process.argv.slice(2))); }
  catch (e) { process.stderr.write(`${e.message}\n`); process.exit(2); }
}

module.exports = { news, parseArgs, pending, watch };
