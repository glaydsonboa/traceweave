from datetime import datetime
from zoneinfo import ZoneInfo

from traceweave.v2.lifecycle import new_chain, resume, start, stop
from traceweave.v2.provenance import (
    compare_bytes,
    custody_mirrored,
    dual_materialized,
    generate_pair,
    record_custody_mirror,
    record_materialization,
)
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


def test_custody_mirror_is_distinct_from_publication_pair():
    source = b"line one\n"
    mirror = record_custody_mirror(
        source_artifact="native/session.jsonl",
        replica_artifact="protected/session.jsonl",
        source=source,
        replica=source,
        native_ids={"receipt": "mirror-001"},
        readback_confirmed=True,
        overwrite_protected=True,
    )
    assert custody_mirrored(mirror)
    assert "pair_key" not in mirror
    assert "github_id" not in mirror
    assert "notion_id" not in mirror


def test_visual_text_similarity_does_not_prove_byte_identity():
    result = compare_bytes(b"same visible line\n", b"same visible line\n\r\n")
    assert not result["same_bytes"]
    assert result["source_bytes"] + 2 == result["replica_bytes"]
    assert result["source_sha256"] != result["replica_sha256"]


def test_chain_verifier_rejects_custody_byte_count_drift():
    chain = new_chain("Example Human", chain_id="custody-chain", created_at="2026-09-22T00:00:00Z")
    start(
        chain,
        session_id="s-custody",
        repository="example/project",
        branch="main",
        head_commit="a" * 40,
        observed_at="2026-09-22T00:00:01Z",
    )
    stop(
        chain,
        session_id="s-custody",
        repository="example/project",
        branch="main",
        head_commit="b" * 40,
        source_artifact="native/session.jsonl",
        source_sha256="4" * 64,
        observed_at="2026-09-22T00:00:02Z",
    )
    mirror = record_custody_mirror(
        source_artifact="native/session.jsonl",
        replica_artifact="protected/session.jsonl",
        source=b"evidence\n",
        replica=b"evidence\n",
        native_ids={"receipt": "mirror-002"},
        readback_confirmed=True,
        overwrite_protected=True,
    )
    chain["custody_mirrors"] = [mirror]
    assert verify_chain(chain).ok

    mirror["replica_bytes"] += 2
    result = verify_chain(chain)
    assert not result.ok
    assert any("byte counts differ" in error for error in result.errors)


def test_source_publication_requires_downloadable_artifact_at_each_destination():
    pair = generate_pair(
        "source publication",
        now=datetime(2026, 9, 22, 1, 2, 3, tzinfo=ZoneInfo("America/Sao_Paulo")),
    )
    sha = "3" * 64
    pub = {
        **pair,
        "source_sha256": sha,
        "public_sha256": sha,
        "transformed": False,
        "artifact_kind": "source",
        "materializations": {},
    }
    record_materialization(
        pub,
        destination="github",
        native_ids={"blob": "abc"},
        public_sha256=sha,
        readback_confirmed=True,
        downloadable_artifact={
            "filename": "example.py",
            "byte_length": 10,
            "sha256": sha,
            "download_reference": "https://example.invalid/example.py",
        },
    )
    record_materialization(
        pub,
        destination="notion",
        native_ids={"file_upload": "def"},
        public_sha256=sha,
        readback_confirmed=True,
    )
    assert not dual_materialized(pub)

    pub["materializations"]["notion"]["downloadable_artifact"] = {
        "filename": "example.py",
        "byte_length": 10,
        "sha256": sha,
        "download_reference": "notion-file-upload:def",
    }
    assert dual_materialized(pub)
