from __future__ import annotations

import json
from pathlib import Path

from polc.cli import _build_projection, main
from polc.model import ProjectionMode

ROOT = Path(__file__).parents[1]
CONFIG = ROOT / "docs" / "configurations" / "cpp20-gcc-application.md"
POLICIES = ROOT / "docs" / "policies"
STANDARD = ROOT / "docs" / "standard"
EXEMPLARS = ROOT / "docs" / "exemplars"


def _build(mode: ProjectionMode):
    return _build_projection(
        CONFIG,
        POLICIES,
        STANDARD,
        EXEMPLARS,
        adapter=None,
        mode=mode,
    )


def test_generation_default_matches_explicit_mode() -> None:
    default, _, _, default_exemplars = _build_projection(
        CONFIG, POLICIES, STANDARD, EXEMPLARS, adapter=None
    )
    explicit, _, _, explicit_exemplars = _build(ProjectionMode.GENERATION)

    assert default.documents() == explicit.documents()
    assert default.sidecar == explicit.sidecar
    assert default_exemplars == explicit_exemplars


def test_modes_share_effective_identity_set() -> None:
    generation, _, _, _ = _build(ProjectionMode.GENERATION)
    review, _, _, _ = _build(ProjectionMode.REVIEW)

    generation_entries = json.loads(generation.sidecar)["entries"]
    review_entries = json.loads(review.sidecar)["entries"]
    assert generation_entries.keys() == review_entries.keys()
    assert generation_entries == review_entries


def test_review_uses_authored_evidence_routes() -> None:
    generation, _, _, _ = _build(ProjectionMode.GENERATION)
    review, _, _, _ = _build(ProjectionMode.REVIEW)

    review_topic = review.topic_documents["writing-a-function"]
    generation_topic = generation.topic_documents["writing-a-function"]
    assert "When the change contains" in review_topic
    assert "a function reads state its parameters and object do not name" in review_topic
    assert "write a function that reaches for global state" not in review_topic
    assert "write a function that reaches for global state" in generation_topic
    assert "a change adds or modifies a function signature" in review.entry
    assert "writing a signature or body" not in review.entry


def test_review_omits_exemplar_documents_and_trees(tmp_path: Path) -> None:
    generation_args = [
        "build",
        "--config",
        str(CONFIG),
        "--policies",
        str(POLICIES),
        "--standard",
        str(STANDARD),
        "--exemplars",
        str(EXEMPLARS),
        "--out",
        str(tmp_path),
    ]
    assert main(generation_args) == 0
    assert (tmp_path / "exemplars.md").is_file()
    assert (tmp_path / "exemplars").is_dir()
    result = main(
        generation_args[:-2] + ["--mode", "review", "--out", str(tmp_path)]
    )

    assert result == 0
    assert not (tmp_path / "exemplars.md").exists()
    assert not (tmp_path / "exemplars").exists()
    assert "exemplars.md" not in (tmp_path / "index.md").read_text(encoding="utf-8")


def test_review_standard_table_exposes_evidence_and_enforcer() -> None:
    review, _, _, _ = _build(ProjectionMode.REVIEW)

    standard = review.standard_documents["standard"]
    assert "| When the change contains | Enforced by | Rule |" in standard
    assert "a C++ source or header uses a nonstandard file extension" in standard
    assert "| review | STD-0001 |" in standard


def test_mode_and_initial_coverage_are_reported() -> None:
    generation, _, _, _ = _build(ProjectionMode.GENERATION)
    review, _, _, _ = _build(ProjectionMode.REVIEW)

    assert json.loads(generation.sidecar)["projection"]["mode"] == "generation"
    assert json.loads(review.sidecar)["projection"]["mode"] == "review"
    assert review.routing_coverage == (18, 266)
    assert generation.routing_coverage[0] > review.routing_coverage[0]


def test_review_claude_adapter_describes_review() -> None:
    projection, _, _, _ = _build_projection(
        CONFIG,
        POLICIES,
        STANDARD,
        EXEMPLARS,
        adapter="claude-code",
        mode=ProjectionMode.REVIEW,
    )

    assert "Use when reviewing existing C++ changes" in projection.entry
    assert "Read before writing or changing" not in projection.entry
