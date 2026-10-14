# Worion: a hash-anchored runtime test of a private AI system

**14 October 2026 · Public evidence summary · Private source under custody**

Worion is Glaydson Boaventura's proprietary AI system, developed under his direction with Claude Code, Codex and DeepSeek. This page reports one controlled end-to-end run. It shows what the preserved runtime records support, where the test contradicted its own hypothesis, and how a reviewer with authorized access can check the original bytes. It does not release Worion's source code, credentials, raw reasoning or unredacted runtime logs.

The question was concrete: when Worion receives a direct question, does the observed route use one answering AI and no external research? When it receives a research question, which AI and source providers actually participate? A model named in configuration was not counted as a call. An attempted provider that failed was not counted as a contributor.

## What was measured

The run identifier is the SHA-256 of the 1,365-byte private run descriptor:

```text
RUN_SHA256=1a0fbc3a50751189f0e7d013a4f2029151c9c4c26730a93b80f3cf0ee07c7630
```

That identifier was visible in the Worion interface and saved console markers. Individual turn files do **not** all contain it as a field. Their relationship to the run was reconstructed through turn IDs, conversation IDs, timestamps, console markers and hashes. The descriptor names source commit `d8589d8cee461812a4d7101fb237c2f729b12b84`; the boot display carried a dirty-worktree marker, so that commit alone cannot reproduce the exact bytes that ran.

Five turns were completed: two initial direct-question attempts, two repeated direct turns and one research turn. The planned second research turn was not executed.

| Turn | Recorded route | Observed model and source activity | Reasoning recorded by J-Lens | Result |
|---|---|---|---:|---|
| `turn-20261014204436-xdd4tt` | Direct | One DeepSeek answering leg; no research cycle in the trace | 2,590 characters | **Proved within the observed trace** |
| `turn-20261014204520-cpx1wk` | Direct | One DeepSeek answering leg; no research cycle in the trace | 906 characters | **Proved within the observed trace** |
| `turn-20261014204751-k1tnu4` | Direct | One DeepSeek answering leg; no research cycle in the trace | 2,375 characters | **Proved within the observed trace** |
| `turn-20261014204830-x5h9zs` | Direct | One DeepSeek answering leg; no research cycle in the trace | 1,121 characters | **Proved within the observed trace** |
| `turn-20261014205016-cgn79l` | Research | DeepSeek in two SSE legs; Gemini grounding in two successful research cycles; Brave in two source calls; two failed Perplexity attempts (HTTP 401) | 3,051 characters in aggregate | **Two AI providers proved; exactly two model calls contradicted** |

For the four direct turns, the answering model recorded by the trace is `deepseek-v4-pro`. For the research turn, the records show two distinct AI providers and four model invocations: two DeepSeek legs and two Gemini grounding cycles. The exact Gemini model name is not established by the runtime records. Brave supplied search results; Perplexity supplied none. The two research cycles produced 43 deduplicated source results in total. These counts describe this run, not every possible Worion route.

The local Cubo recorded retrieved items in all five turns but was in shadow mode (`influenced_response=false`). In the research tool, a separate Cubo ranking step reordered the source pool. J-Lens recorded the presence and size of reasoning. The final reasoning text is preserved for each direct turn and for the final research cycle. The first research cycle is represented by its length and SHA-256 in the completion record, but its full text was not recovered from the inspected artifacts. None of the five traces proves persisted J-Lens learning.

## Custody chain

The private evidence package has 129 files. Its `SHA256SUMS` list has 129 entries; all 129 file hashes were recalculated successfully on 14 October 2026. The public [evidence index](public-evidence-index.json) gives byte counts and SHA-256 values for the run descriptor, package manifest, checksum list, saved console, two original screenshots and seven record classes for each of the five turns. It contains no raw turn content or local filesystem paths.

| Link in the chain | Private record used | What it establishes |
|---|---|---|
| Question and route | Conversation, composer trace, turn trace and ledger | The submitted question, chosen route, turn ID and conversation ID |
| Model and research activity | Turn trace and SSE timing | Observed answering legs, research cycles, provider results and failures |
| Reasoning and answer | Conversation envelope and completion record | Preserved final reasoning, answer text, lengths and content hashes |
| Persistence and completion | Conversation file, completion seal, ledger and console | A completed turn with correlated persisted records |
| Visible run marker | Original UI captures and saved console | The run identifier displayed to the operator and printed during the run |

The checksum list itself has SHA-256 `75727ab843fac4b58afcdd845aea74417237ba0f6590d82632b6055f498cc8a6`. The private manifest has SHA-256 `841fc3a526bc010596a14f8de9dd0b0af046db204a65e8067c30942538e445c4`. These hashes commit to bytes; by themselves they do not authenticate the runtime or reveal the content of a private file.

The saved console provides a second, independent way to locate the turn records. These are selected fields transcribed from its original lines; the SHA-256 of the complete, private console is in the evidence index. Line numbers refer to that saved file, not to this page.

| Console line | Marker | Turn | Selected recorded fields |
|---:|---|---|---|
| 66 | `JLENS ADMISSION` | `turn-20261014204436-xdd4tt` | `reasoning_chars=2590 reasoning_present=true` |
| 111 | `JLENS ADMISSION` | `turn-20261014204520-cpx1wk` | `reasoning_chars=906 reasoning_present=true` |
| 167 | `JLENS ADMISSION` | `turn-20261014204751-k1tnu4` | `reasoning_chars=2375 reasoning_present=true` |
| 212 | `JLENS ADMISSION` | `turn-20261014204830-x5h9zs` | `reasoning_chars=1121 reasoning_present=true` |
| 264 | `JLENS ADMISSION` | `turn-20261014205016-cgn79l` | `reasoning_chars=3051 reasoning_present=true` |
| 273 | `TURN SUMMARY` | `turn-20261014205016-cgn79l` | `route=research_team research=true errors=0 warnings=0` |

An authorized reviewer who receives the private package can run [verify-private-bundle.py](verify-private-bundle.py) against the public index. It checks the 129 listed files and the 35 indexed per-turn records without printing their contents. A public reader can inspect the index and method, but cannot independently reproduce the private runtime from this page alone.

## Size of the versioned codebase

At the declared source commit, the published [scope](source-line-scope.json) and [generic counter](count-source-lines.py) measure **244,922 physical lines across 1,001 tracked source-like files**:

| Scope | Files | Physical lines |
|---|---:|---:|
| Application, services and CLI | 283 | 120,630 |
| Automation and migrations | 300 | 67,007 |
| Tests | 418 | 57,285 |

The count includes blank lines and comments. It excludes documentation, runtime data and the generated, archive, vendor and build paths named in the published scope. It is a Git-tree measurement at `d8589d8c…`, not a measurement of the dirty runtime worktree. Git does not prove which model wrote each line, so **244,922 is not a claim of 244,922 AI-generated lines**. It describes the codebase built through this human-directed, multi-agent workflow. The exact output is preserved in [source-line-result.json](source-line-result.json).

## What this proof does not claim

- The research hypothesis of **exactly two model calls** failed. The observed research turn used two AI providers across four invocations.
- A second research turn was planned but not run.
- The first research reasoning cycle has a recorded hash and length, but its complete text is not available in the inspected files.
- A screenshot corroborates what the interface displayed; it is not a substitute for native runtime records.
- The public index is a custody map for a private bundle. Public hashes do not make private source code publicly reproducible.

Raw source, environment files, internal paths, complete logs, prompts, reasoning and the original screenshots remain in the private repository or private evidence custody. The original captures contain account identity, conversation titles and local paths, so they are intentionally absent here. A reviewer may request controlled access to the originals and compare them against the public hashes. The code examples on this page are independent verification tools, not excerpts from Worion's proprietary implementation.
