"""
Anthropic-compatible tool-pairing smoke test.

Checks:
1. endpoint reachability;
2. first tool_use;
3. tool_result round-trip;
4. second tool_use in the same conversation;
5. second tool_use.id differs from the first.

No shell command is executed. The "pwd" tool is simulated locally.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error


def post(url: str, key: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url.rstrip("/") + "/v1/messages",
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {exc.code}: {body[:2000]}") from exc


def first_tool_use(message: dict) -> dict:
    for block in message.get("content") or []:
        if block.get("type") == "tool_use":
            return block
    raise RuntimeError(f"No tool_use block returned: {json.dumps(message)[:2000]}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--api-key", required=True)
    ap.add_argument("--model", required=True)
    args = ap.parse_args()

    tool = {
        "name": "pwd",
        "description": "Return the current working directory.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    }

    messages = [
        {
            "role": "user",
            "content": "Call the pwd tool exactly once. Do not answer without calling it.",
        }
    ]

    first = post(
        args.base_url,
        args.api_key,
        {
            "model": args.model,
            "max_tokens": 1024,
            "tools": [tool],
            "messages": messages,
        },
    )
    t1 = first_tool_use(first)

    messages.append({"role": "assistant", "content": first["content"]})
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": t1["id"],
                    "content": "/traceweave/smoke/round-1",
                },
                {
                    "type": "text",
                    "text": "Now call the pwd tool exactly once again.",
                },
            ],
        }
    )

    second = post(
        args.base_url,
        args.api_key,
        {
            "model": args.model,
            "max_tokens": 1024,
            "tools": [tool],
            "messages": messages,
        },
    )
    t2 = first_tool_use(second)

    print(f"round_1_tool_use_id={t1['id']}")
    print(f"round_2_tool_use_id={t2['id']}")

    if t1["id"] == t2["id"]:
        print("FAIL: duplicate tool_use.id across separate tool calls", file=sys.stderr)
        return 2

    print("PASS: tool-use IDs are distinct across two rounds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
