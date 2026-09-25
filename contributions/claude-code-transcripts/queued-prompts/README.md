# Prompts typed while Claude is working

Upstream issue [#98](https://github.com/simonw/claude-code-transcripts/issues/98) · pull request [#118](https://github.com/simonw/claude-code-transcripts/pull/118)

## The problem

If you type while Claude Code is working, your prompt goes into a queue. The session file records it twice:

1. `queue-operation` / `enqueue`, when the prompt enters the queue.
2. Its delivery, in one of two forms:
   - an `attachment` entry with `attachment.type: "queued_command"` and `commandMode: "prompt"`, when Claude takes it in mid-turn;
   - an ordinary `user` entry, when it is sent after the turn ends.

The exporter reads only `user` and `assistant` entries, so every prompt taken in mid-turn disappears from the transcript.

## The fix

[`keep-queued-prompts.patch`](keep-queued-prompts.patch) turns each human `queued_command` attachment into a user entry. It reads the delivery record rather than the enqueue record, so a prompt is never shown twice. Background task notifications use `commandMode: "task-notification"` and entries with a non-human `origin`; both stay out.

Another open pull request, [#112](https://github.com/simonw/claude-code-transcripts/pull/112), reads the enqueue record instead. Its author notes that a prompt can then appear twice when it is also delivered as an ordinary user entry.

## Checking it on your own sessions

[`account_queued_prompts.py`](account_queued_prompts.py) matches every queued prompt to its delivery record and prints counts only, never text:

```sh
python account_queued_prompts.py ~/.claude/projects/<project>/*.jsonl
```

```json
{
  "sessions": 3,
  "enqueued": 63,
  "delivered_mid_turn": 25,
  "delivered_as_user_message": 36,
  "delivered_with_changes": 1,
  "not_delivered": 1
}
```

That is the result on the sessions where the problem was found. The unpatched exporter misses the prompts delivered mid-turn. With the patch, only the two in the last two lines are not shown exactly as queued.

[`example-session.jsonl`](example-session.jsonl) is a synthetic session with one of each case. It is used by `tests/test_contrib_claude_code_transcripts.py`.
