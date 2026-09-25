"""Account for every prompt typed while Claude Code was working.

Claude Code records a prompt typed mid-turn twice: once when it enters the
queue (`queue-operation` / `enqueue`) and once when it is delivered. Delivery
is either an `attachment` entry with `attachment.type == "queued_command"`
(taken in mid-turn) or an ordinary `user` entry (sent after the turn ended).

A transcript exporter that reads only `user` entries loses the first kind.
This tool matches each enqueued prompt to its delivery record and reports
counts only, so it can run on private sessions without printing their text.

A prompt can also be delivered with more text than was queued, for example
when pasted content is expanded. Those are counted as
`delivered_with_changes` when a user entry containing the queued text starts
within a few seconds of the enqueue.

Usage:
    python account_queued_prompts.py SESSION.jsonl [SESSION.jsonl ...]
"""

import json
import sys
from collections import Counter
from datetime import datetime

TASK_NOTIFICATION = "<task-notification>"
DELIVERY_WINDOW_SECONDS = 5


def _time(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def _user_text(entry):
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def _mid_turn_prompt(entry):
    attachment = entry.get("attachment") or {}
    if attachment.get("type") != "queued_command":
        return None
    if attachment.get("commandMode") != "prompt":
        return None
    origin = attachment.get("origin")
    if isinstance(origin, dict) and origin.get("kind") not in (None, "human"):
        return None
    prompt = attachment.get("prompt")
    return prompt if isinstance(prompt, str) else None


def _delivered_with_changes(text, queued_at, user_entries):
    if queued_at is None:
        return False
    for other, sent_at in user_entries:
        if sent_at is None or text not in other or other == text:
            continue
        if 0 <= (sent_at - queued_at).total_seconds() <= DELIVERY_WINDOW_SECONDS:
            return True
    return False


def account(lines):
    """Return counts for one session, given its JSONL lines."""
    enqueued, mid_turn, user_messages, user_entries = [], Counter(), Counter(), []
    for line in lines:
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = entry.get("type")
        if kind == "queue-operation" and entry.get("operation") == "enqueue":
            content = entry.get("content")
            if isinstance(content, str) and not content.lstrip().startswith(
                TASK_NOTIFICATION
            ):
                enqueued.append((content.strip(), _time(entry.get("timestamp"))))
        elif kind == "attachment":
            prompt = _mid_turn_prompt(entry)
            if prompt is not None:
                mid_turn[prompt.strip()] += 1
        elif kind == "user":
            text = _user_text(entry).strip()
            if text:
                user_messages[text] += 1
                user_entries.append((text, _time(entry.get("timestamp"))))

    counts = Counter(enqueued=len(enqueued))
    for text, queued_at in enqueued:
        if mid_turn[text] > 0:
            mid_turn[text] -= 1
            counts["delivered_mid_turn"] += 1
        elif user_messages[text] > 0:
            user_messages[text] -= 1
            counts["delivered_as_user_message"] += 1
        elif _delivered_with_changes(text, queued_at, user_entries):
            counts["delivered_with_changes"] += 1
        else:
            counts["not_delivered"] += 1
    return counts


def main(paths):
    total = Counter()
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            counts = account(handle)
        if counts["enqueued"]:
            total["sessions"] += 1
            total.update(counts)
    keys = (
        "sessions",
        "enqueued",
        "delivered_mid_turn",
        "delivered_as_user_message",
        "delivered_with_changes",
        "not_delivered",
    )
    print(json.dumps({key: total.get(key, 0) for key in keys}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
