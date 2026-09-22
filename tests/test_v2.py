from datetime import datetime
from zoneinfo import ZoneInfo

from traceweave.v2.lifecycle import new_chain, resume, start, stop
from traceweave.v2.provenance import dual_materialized, generate_pair, record_materialization
from traceweave.v2.verify import verify_chain


def test_lifecycle_hash_chain_and_resume_anchor():
    chain = new_chain("Example Human", chain_id="chain-test", created_at="2026-09-22T00:00:00Z")
    first = start(
        chain,
        session_id="s1",
        repository="example/project",
        branch="main",
        head_commit="a" * 40,
        observed_at="2026-09-22T00:00:01Z",
    )
    resume(
        chain,
        session_id="s1",
        repository="example/project",
        branch="main",
        head_commit="b" * 40,
        resume_from_event_sha256=first["event_sha256"],
        observed_at="2026-09-22T00:00:02Z",
    )
    stop(
        chain,
        session_id="s1",
        repository="example/project",
        branch="main",
        head_commit="c" * 40,
        source_artifact="records/transcript.md",
        source_sha256="d" * 64,
        observed_at="2026-09-22T00:00:03Z",
    )
    result = verify_chain(chain)
    assert result.ok, result.errors
    assert chain["status"] == "closed"


def test_pair_generation_shares_one_key():
    pair = generate_pair(
        "publish causal chain",
        now=datetime(2026, 9, 22, 1, 2, 3, tzinfo=ZoneInfo("America/Sao_Paulo")),
    )
    assert pair["pair_key"] == "20260922-010203-publish-causal-chain"
    assert pair["github_id"].endswith(pair["pair_key"])
    assert pair["notion_id"].endswith(pair["pair_key"])


def test_dual_materialization_requires_native_ids_and_readback():
    pair = generate_pair(
        "document",
        now=datetime(2026, 9, 22, 1, 2, 3, tzinfo=ZoneInfo("America/Sao_Paulo")),
    )
    pub = {
        **pair,
        "source_sha256": "1" * 64,
        "public_sha256": "2" * 64,
        "transformed": True,
        "materializations": {},
    }
    record_materialization(
        pub,
        destination="github",
        native_ids={"commit": "abc", "blob": "def"},
        public_sha256="2" * 64,
        readback_confirmed=True,
    )
    assert not dual_materialized(pub)
    record_materialization(
        pub,
        destination="notion",
        native_ids={"block_id": "ghi"},
        public_sha256="2" * 64,
        readback_confirmed=True,
    )
    assert dual_materialized(pub)
