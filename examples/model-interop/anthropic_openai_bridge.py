"""
Minimal Anthropic Messages -> OpenAI Chat Completions compatibility bridge.

Purpose:
    Let an Anthropic-Messages client such as Claude Code talk to a provider that
    exposes an OpenAI-compatible Chat Completions API (for example Gemini).

This is protocol translation, not model impersonation.

Design choices:
- binds to 127.0.0.1 by default;
- trusts local clients and does not validate their incoming API key;
- rejects unsupported image/document blocks instead of silently dropping them;
- translates tool_use/tool_result pairs;
- buffers upstream output and emits Anthropic-style SSE when stream=true;
- does not emulate Anthropic beta APIs, prompt caching or computer-use contracts.

Environment:
    UPSTREAM_API_KEY          required
    UPSTREAM_BASE_URL         default: Gemini OpenAI compatibility endpoint
    UPSTREAM_MODEL            required for production use
    UPSTREAM_REASONING_EFFORT optional provider-compatible value
    BRIDGE_PORT               default: 4010
"""

from __future__ import annotations

import json
import os
import uuid
from typing import Any, Iterable

import httpx
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI(title="Traceweave Model Interop Bridge", version="0.1")

UPSTREAM_BASE_URL = os.getenv(
    "UPSTREAM_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai",
).rstrip("/")
UPSTREAM_MODEL = os.getenv("UPSTREAM_MODEL", "").strip()
UPSTREAM_REASONING_EFFORT = os.getenv("UPSTREAM_REASONING_EFFORT", "").strip()


def _text_from_system(system: Any) -> str:
    if system is None:
        return ""
    if isinstance(system, str):
        return system
    if isinstance(system, list):
        chunks: list[str] = []
        for block in system:
            if not isinstance(block, dict):
                raise HTTPException(400, "Unsupported system block.")
            if block.get("type") != "text":
                raise HTTPException(400, f"Unsupported system block type: {block.get('type')}")
            chunks.append(str(block.get("text", "")))
        return "\n".join(chunks)
    raise HTTPException(400, "Unsupported system format.")


def _anthropic_tools_to_openai(tools: list[dict[str, Any]] | None) -> list[dict[str, Any]] | None:
    if not tools:
        return None
    out = []
    for tool in tools:
        out.append(
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("input_schema") or {"type": "object", "properties": {}},
                },
            }
        )
    return out


def _tool_choice_to_openai(choice: Any) -> Any:
    if not choice:
        return None
    if isinstance(choice, str):
        return choice
    if not isinstance(choice, dict):
        return None
    kind = choice.get("type")
    if kind == "auto":
        return "auto"
    if kind == "any":
        return "required"
    if kind == "none":
        return "none"
    if kind == "tool" and choice.get("name"):
        return {"type": "function", "function": {"name": choice["name"]}}
    return None


def _assistant_blocks_to_openai(content: list[dict[str, Any]]) -> dict[str, Any]:
    text_parts: list[str] = []
    tool_calls: list[dict[str, Any]] = []

    for block in content:
        kind = block.get("type")
        if kind == "text":
            text_parts.append(str(block.get("text", "")))
        elif kind == "tool_use":
            call_id = str(block.get("id") or f"toolu_{uuid.uuid4().hex}")
            tool_calls.append(
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": str(block.get("name", "")),
                        "arguments": json.dumps(block.get("input") or {}, ensure_ascii=False),
                    },
                }
            )
        elif kind in {"thinking", "redacted_thinking"}:
            continue
        else:
            raise HTTPException(400, f"Unsupported assistant block type: {kind}")

    msg: dict[str, Any] = {"role": "assistant", "content": "\n".join(text_parts) or None}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return msg


def _user_blocks_to_openai(content: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    buffered_text: list[str] = []

    def flush_text() -> None:
        if buffered_text:
            out.append({"role": "user", "content": "\n".join(buffered_text)})
            buffered_text.clear()

    for block in content:
        kind = block.get("type")
        if kind == "text":
            buffered_text.append(str(block.get("text", "")))
        elif kind == "tool_result":
            flush_text()
            value = block.get("content", "")
            if isinstance(value, list):
                parts = []
                for sub in value:
                    if isinstance(sub, dict) and sub.get("type") == "text":
                        parts.append(str(sub.get("text", "")))
                    else:
                        raise HTTPException(400, "Unsupported nested tool_result content.")
                value = "\n".join(parts)
            elif not isinstance(value, str):
                value = json.dumps(value, ensure_ascii=False)
            out.append(
                {
                    "role": "tool",
                    "tool_call_id": str(block.get("tool_use_id", "")),
                    "content": value,
                }
            )
        elif kind in {"image", "document"}:
            raise HTTPException(
                400,
                f"Block type '{kind}' is not supported by this minimal bridge; refusing to drop it silently.",
            )
        else:
            raise HTTPException(400, f"Unsupported user block type: {kind}")

    flush_text()
    return out


def _messages_to_openai(body: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    system = _text_from_system(body.get("system"))
    if system:
        out.append({"role": "system", "content": system})

    for msg in body.get("messages") or []:
        role = msg.get("role")
        content = msg.get("content", "")
        if isinstance(content, str):
            out.append({"role": role, "content": content})
            continue
        if not isinstance(content, list):
            raise HTTPException(400, "Unsupported message content format.")

        if role == "assistant":
            out.append(_assistant_blocks_to_openai(content))
        elif role == "user":
            out.extend(_user_blocks_to_openai(content))
        else:
            raise HTTPException(400, f"Unsupported role: {role}")

    return out


def _parse_tool_arguments(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    if raw in (None, ""):
        return {}
    try:
        parsed = json.loads(str(raw))
    except json.JSONDecodeError:
        return {"_raw": str(raw)}
    return parsed if isinstance(parsed, dict) else {"value": parsed}


def _openai_to_anthropic(response: dict[str, Any], requested_model: str) -> dict[str, Any]:
    choices = response.get("choices") or []
    if not choices:
        raise HTTPException(502, "Upstream returned no choices.")

    message = choices[0].get("message") or {}
    blocks: list[dict[str, Any]] = []

    text = message.get("content")
    if text:
        blocks.append({"type": "text", "text": str(text)})

    for call in message.get("tool_calls") or []:
        fn = call.get("function") or {}
        blocks.append(
            {
                "type": "tool_use",
                "id": str(call.get("id") or f"toolu_{uuid.uuid4().hex}"),
                "name": str(fn.get("name", "")),
                "input": _parse_tool_arguments(fn.get("arguments")),
            }
        )

    finish_reason = choices[0].get("finish_reason")
    stop_reason = "tool_use" if any(b["type"] == "tool_use" for b in blocks) else "end_turn"
    if finish_reason == "length":
        stop_reason = "max_tokens"

    usage = response.get("usage") or {}
    return {
        "id": f"msg_{uuid.uuid4().hex}",
        "type": "message",
        "role": "assistant",
        "model": requested_model,
        "content": blocks,
        "stop_reason": stop_reason,
        "stop_sequence": None,
        "usage": {
            "input_tokens": int(usage.get("prompt_tokens") or 0),
            "output_tokens": int(usage.get("completion_tokens") or 0),
        },
    }


def _sse_event(event: str, data: dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def _anthropic_sse(message: dict[str, Any]) -> Iterable[str]:
    start = dict(message)
    start["content"] = []
    start["stop_reason"] = None
    start["stop_sequence"] = None
    start["usage"] = {"input_tokens": message["usage"]["input_tokens"], "output_tokens": 0}
    yield _sse_event("message_start", {"type": "message_start", "message": start})

    for index, block in enumerate(message["content"]):
        if block["type"] == "text":
            yield _sse_event(
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": index,
                    "content_block": {"type": "text", "text": ""},
                },
            )
            yield _sse_event(
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": index,
                    "delta": {"type": "text_delta", "text": block["text"]},
                },
            )
        elif block["type"] == "tool_use":
            yield _sse_event(
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": index,
                    "content_block": {
                        "type": "tool_use",
                        "id": block["id"],
                        "name": block["name"],
                        "input": {},
                    },
                },
            )
            yield _sse_event(
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": index,
                    "delta": {
                        "type": "input_json_delta",
                        "partial_json": json.dumps(block["input"], ensure_ascii=False),
                    },
                },
            )
        yield _sse_event(
            "content_block_stop",
            {"type": "content_block_stop", "index": index},
        )

    yield _sse_event(
        "message_delta",
        {
            "type": "message_delta",
            "delta": {
                "stop_reason": message["stop_reason"],
                "stop_sequence": None,
            },
            "usage": {"output_tokens": message["usage"]["output_tokens"]},
        },
    )
    yield _sse_event("message_stop", {"type": "message_stop"})


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "ok": True,
        "upstream_base_url": UPSTREAM_BASE_URL,
        "upstream_model": UPSTREAM_MODEL or "NOT_SET",
        "protocol_in": "anthropic-messages",
        "protocol_out": "openai-chat-completions",
    }


@app.post("/v1/messages")
async def messages(
    body: dict[str, Any],
    x_api_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
):
    del x_api_key, authorization

    upstream_key = os.getenv("UPSTREAM_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not upstream_key:
        raise HTTPException(500, "UPSTREAM_API_KEY (or GEMINI_API_KEY) is not set.")
    if not UPSTREAM_MODEL:
        raise HTTPException(500, "UPSTREAM_MODEL is not set.")

    requested_model = str(body.get("model") or UPSTREAM_MODEL)
    messages_openai = _messages_to_openai(body)

    payload: dict[str, Any] = {
        "model": UPSTREAM_MODEL,
        "messages": messages_openai,
        "max_tokens": int(body.get("max_tokens") or 8192),
        "stream": False,
    }

    tools = _anthropic_tools_to_openai(body.get("tools"))
    if tools:
        payload["tools"] = tools

    tool_choice = _tool_choice_to_openai(body.get("tool_choice"))
    if tool_choice is not None:
        payload["tool_choice"] = tool_choice

    if UPSTREAM_REASONING_EFFORT:
        payload["reasoning_effort"] = UPSTREAM_REASONING_EFFORT

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{UPSTREAM_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {upstream_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
    except httpx.HTTPError as exc:
        raise HTTPException(502, f"Upstream request failed: {exc}") from exc

    if response.status_code >= 400:
        detail = response.text[:4000]
        raise HTTPException(response.status_code, f"Upstream error: {detail}")

    try:
        upstream = response.json()
    except ValueError as exc:
        raise HTTPException(502, "Upstream returned invalid JSON.") from exc

    message = _openai_to_anthropic(upstream, requested_model)

    headers = {
        "x-traceweave-effective-provider": "openai-compatible",
        "x-traceweave-effective-model": UPSTREAM_MODEL,
    }

    if body.get("stream"):
        return StreamingResponse(
            _anthropic_sse(message),
            media_type="text/event-stream",
            headers=headers,
        )

    return JSONResponse(message, headers=headers)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("BRIDGE_PORT", "4010"))
    uvicorn.run(app, host="127.0.0.1", port=port)
