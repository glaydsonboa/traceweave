# From a Private MCP Server to OpenAI

## An evidence-backed operating protocol for Secure MCP Tunnel

## The problem that emerged

A local MCP server worked over `stdio`, but hosted OpenAI products could not reach a process that
existed only inside a private machine. Publishing the server on a public HTTPS endpoint would have
changed the security boundary merely to solve reachability.

The transport problem had an official solution: OpenAI Secure MCP Tunnel. The operational problem
remained:

- a configured tunnel was not proof that its client was running;
- a running process was not proof that it was ready or polling;
- a ready tunnel was not proof that the intended OpenAI workspace could discover it;
- a discovered MCP server was not proof that a tool call completed;
- restarting blindly could create duplicate clients and orphaned processes;
- storing a runtime key in a profile, command history, or log would turn connectivity into a secret-management failure.

The failure was not the tunnel protocol. It was the gap between configuration, runtime state and
observable completion.

## What OpenAI provides

[Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) keeps a private
MCP server behind its existing network boundary. A customer-run `tunnel-client` opens an outbound
HTTPS connection to OpenAI, receives queued MCP work, forwards the JSON-RPC request to the approved
local server and returns the response through the same path.

No inbound firewall port is required. The private MCP server may be reached locally through `stdio`
or through an HTTP address available inside the same trust boundary.

## What Traceweave resolved

Traceweave does not replace or reimplement Secure MCP Tunnel. It turns the integration into a
recoverable operating protocol whose state can be checked without trusting a conversational report.

The protocol separates these claims:

```text
tunnel created
    != profile configured
    != client running
    != client ready
    != OpenAI surface connected
    != MCP tool invocation completed
```

Each transition requires its own evidence. If that evidence was not observed, the state remains
`unknown`.

## Evidence ledger

| Public claim | Evidence class | Public source | Limit |
|---|---|---|---|
| `tunnel-client` connects outward and forwards MCP work to a private server | `DOCUMENTED` | OpenAI Secure MCP Tunnel documentation | Documentation proves the supported design, not a specific deployment |
| a tunnel may target a local `stdio` command or an internal HTTP MCP server | `DOCUMENTED` | OpenAI Secure MCP Tunnel documentation | Local reachability still has to be tested |
| `/healthz`, `/readyz`, `/metrics` and `/ui` expose local operational state | `DOCUMENTED` | OpenAI Secure MCP Tunnel documentation | A previous successful check does not prove current readiness |
| ChatGPT, Codex and the Responses API can use a supported tunnel association | `DOCUMENTED` | OpenAI MCP documentation | Availability and permissions depend on the target organization or workspace |
| Traceweave separates configuration, readiness, discovery and completed invocation | `DOCUMENTED` | this versioned protocol and its state model | The protocol defines the checks; it does not manufacture their results |
| a particular private tunnel completed an end-to-end call | `UNKNOWN` in this public artifact | intentionally omitted | Requires a current sanitized runtime record from that deployment |

No private transcript, runtime key, tunnel identifier, local path or internal topology is used as
public proof. The external claims can be checked against the primary sources; deployment claims must
be reproduced in the target environment.

## Causal chain

```text
OpenAI tunnel record
    -> organization and workspace association
    -> local tunnel-client profile
    -> runtime key supplied to the process
    -> tunnel-client started
    -> local readiness observed
    -> OpenAI surface connected by tunnel_id
    -> MCP tool discovered
    -> representative tool call completed
    -> result recorded
```

The chain identifies the first missing transition instead of collapsing every failure into
"the tunnel is broken."

## Protocol

### 1. Freeze the boundary

Record, without secrets:

- the private MCP transport: `stdio` or internal HTTP;
- the command or private URL that `tunnel-client` may reach;
- the OpenAI Platform organization that owns the tunnel;
- every ChatGPT workspace or additional Platform organization allowed to use it;
- the operator responsible for the local client process;
- the expected evidence for readiness and for one completed MCP call.

Do not widen the local server's network exposure as part of this step.

### 2. Create and associate the tunnel

Create the tunnel in OpenAI Platform tunnel settings. Associate it with the Platform organization
that owns it and with each ChatGPT workspace or additional Platform organization that must discover
it.

Preserve the returned `tunnel_id` as configuration identity, not as a secret. Do not publish a real
identifier in examples or screenshots.

Platform tunnel permissions and ChatGPT developer-mode access are separate. Tunnel creation requires
the relevant tunnel management permission; running or selecting it requires tunnel use permission.

### 3. Install and configure `tunnel-client`

Use the current release linked from the OpenAI tunnel settings or official documentation. Keep the
runbook pointed at the current release instead of embedding a version-specific download URL.

For a local `stdio` MCP server:

```bash
export CONTROL_PLANE_API_KEY="<runtime-key>"

tunnel-client init \
  --sample sample_mcp_stdio_local \
  --profile private-mcp \
  --tunnel-id tunnel_<redacted> \
  --mcp-command "<absolute command that starts the MCP server>"
```

For an internal HTTP MCP server, configure its private MCP URL instead of `--mcp-command`:

```bash
tunnel-client init \
  --profile private-mcp \
  --tunnel-id tunnel_<redacted> \
  --mcp-server-url http://127.0.0.1:<port>/mcp
```

The profile contains routing configuration. The runtime key should be injected into the process
environment and kept out of the profile, repository, command transcript and logs.

### 4. Validate before starting

```bash
tunnel-client doctor --profile private-mcp --explain
```

Capture the command, client version, timestamp and result. A successful diagnostic proves the
validated conditions reported by `doctor`; it does not prove that the long-running client remains
connected afterward.

### 5. Start exactly one client

Before starting a new process, query the local readiness endpoint. Start a client only when no ready
instance already owns the profile.

```bash
tunnel-client run --profile private-mcp
```

The runtime key should enter through the child process environment. Standard output and standard
error may be redirected to a restricted operational log, but raw HTTP logging and secret-bearing
environment dumps must remain disabled.

The process that starts `tunnel-client` owns its lifecycle until verified shutdown or an explicit
transfer to a service manager.

### 6. Prove readiness

The client exposes local operational surfaces, loopback-only by default:

```text
/healthz  -> process health
/readyz   -> readiness to handle tunnel work
/metrics  -> operational metrics
/ui       -> local administration view
```

Poll `/readyz` with a bounded timeout. Record the HTTP status and observation time. A process ID
alone is insufficient: a live process may still be disconnected, misconfigured or unable to poll.

Recommended transition:

```text
STARTING --(/readyz = 200)--> READY
STARTING --(timeout)--------> DEGRADED
```

### 7. Connect the OpenAI surface

For a ChatGPT developer-mode app, choose **Tunnel** as the connection type and select the associated
tunnel or enter its `tunnel_id`. Confirm that the expected MCP tools are discovered.

For the Responses API, use `tunnel_id` in the MCP tool definition. Do not pass the OpenAI-hosted
tunnel endpoint as `server_url`:

```json
{
  "type": "mcp",
  "server_label": "private_mcp",
  "tunnel_id": "tunnel_<redacted>"
}
```

Use `server_url` only when the MCP server itself is directly reachable by the API.

### 8. Prove one complete invocation

Tool discovery proves metadata exchange, not execution. Run one representative, bounded tool call
and retain:

- the OpenAI surface used;
- the tool name;
- sanitized arguments;
- approval behavior;
- result or error;
- start and completion timestamps;
- the local tunnel readiness observation nearest to the call;
- a content hash for any persisted result when byte identity matters.

Only this step promotes the integration from `CONNECTED` to `VERIFIED`.

### 9. Stop or transfer ownership

An interactive client must be stopped and its termination verified. A persistent client must be
transferred to an explicit owner such as `systemd`, a Windows service, a container supervisor or a
Kubernetes controller.

Do not treat a detached process as managed merely because it survived its launcher. Record:

```text
owner
process identity
profile
started_at
last readiness observation
shutdown or transfer result
```

On resume, recheck the process owner and `/readyz`; do not infer readiness from the previous session.

## State model

| State | Minimum evidence |
|---|---|
| `ABSENT` | no tunnel identity recorded |
| `CONFIGURED` | tunnel identity and local profile exist |
| `VALIDATED` | `doctor` result observed for that profile |
| `STARTING` | client process creation observed |
| `READY` | bounded `/readyz` check returned success |
| `CONNECTED` | target OpenAI surface discovered the MCP tools |
| `VERIFIED` | one representative tool call completed |
| `DEGRADED` | process or configuration exists, but a required transition failed |
| `STOPPED` | termination observed or ownership transfer verified |
| `UNKNOWN` | required evidence was not observed |

## Failure isolation

| Symptom | Check first | Claim that must not be made yet |
|---|---|---|
| tunnel is absent from ChatGPT | workspace association and tunnel use permission | "the local MCP is broken" |
| tools are not discovered | `tunnel-client` process, `/readyz`, profile target | "the tool schema is invalid" |
| tool is listed but invocation fails | local MCP logs and representative call trace | "the tunnel is down" |
| a second launcher refuses to start | existing ready owner for the profile | "the process is orphaned" |
| process exists but `/readyz` fails | polling connection, key, network and profile | "the tunnel is connected" |
| API request uses `server_url` for a tunnel | replace it with `tunnel_id` | "Secure MCP Tunnel is unsupported" |

## Security boundary

- The tunnel is transport. It does not replace tool-level authorization.
- The runtime key authenticates `tunnel-client` to the OpenAI control plane; it must not become a tool argument.
- Workspace association limits discovery but does not remove the need for least-privilege MCP tools.
- Write or publish tools should retain explicit approval and independent scope checks where required.
- The local admin UI should remain loopback-only unless an operator network intentionally exposes it.
- OAuth discovery may traverse the tunnel, but the authorization server is not automatically tunneled.
- Logs and screenshots must be sanitized before publication.

## Reproducibility record

The following compact record is sufficient for a later session to distinguish known state from
narration:

```json
{
  "tunnel_id": "redacted-content-identity",
  "profile": "private-mcp",
  "client_version": "observed-version",
  "transport": "stdio",
  "doctor": {
    "observed_at": "RFC3339 timestamp",
    "status": "passed | failed | unknown"
  },
  "readiness": {
    "observed_at": "RFC3339 timestamp",
    "http_status": 200
  },
  "surface": "ChatGPT | Codex | Responses API",
  "tool_discovery": "observed | not_observed | unknown",
  "invocation": {
    "tool": "sanitized tool name",
    "completed": true,
    "evidence": "sanitized reference or hash"
  },
  "process_cleanup": "confirmed | transferred | unknown"
}
```

Do not store the runtime API key, private MCP URL, local filesystem path or unrestricted logs in this
record.

## Limits

Secure MCP Tunnel is suitable for private connections and developer-mode testing. It is not the
public endpoint required for public plugin submission. Public distribution requires the deployment
and authentication boundaries described by the current OpenAI plugin documentation.

This document proves a protocol and its evidence requirements. It does not prove that any particular
tunnel is currently online. That claim requires a current readiness observation and a completed call
from the intended OpenAI surface.

## Primary sources

Source cutoff: 2026-09-30.

- [Secure MCP Tunnel — OpenAI Developers](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
- [MCP servers — OpenAI API](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)
- [Connect and test your plugin — OpenAI Developers](https://developers.openai.com/plugins/deploy/connect-chatgpt)
