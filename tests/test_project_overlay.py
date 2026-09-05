from __future__ import annotations

import json
from pathlib import Path

import pytest

from polc.cli import _build_project_projection, _build_projection
from polc.config import load_project_configuration
from polc.corpus import overlay_fingerprint
from polc.model import PolcError

ROOT = Path(__file__).parents[1]
POLICIES = ROOT / "docs" / "policies"
STANDARD = ROOT / "docs" / "standard"
EXEMPLARS = ROOT / "docs" / "exemplars"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _project(
    root: Path,
    *,
    exclude_topics: str = "[]",
    exclude_ids: str = "[]",
    replace_ids: str = "[]",
) -> Path:
    path = root / ".polc" / "project.md"
    _write(
        path,
        f"""---
name: cpp20-gcc-application
language_version: 20
compiler: gcc
domain: application
exclude_topics: {exclude_topics}
exclude_ids: {exclude_ids}
replace_ids: {replace_ids}
---

# Overlay test
""",
    )
    return path


def _build(project: Path):
    return _build_project_projection(
        project, POLICIES, STANDARD, EXEMPLARS, adapter=None
    )


def test_empty_overlay_builds_with_overlay_identity(tmp_path: Path) -> None:
    projection, _, config, _ = _build(_project(tmp_path))
    legacy, _, _, _ = _build_projection(
        ROOT / "docs" / "configurations" / "cpp20-gcc-application.md",
        POLICIES,
        STANDARD,
        EXEMPLARS,
        adapter=None,
    )

    provenance = json.loads(projection.sidecar)
    assert config.name == "cpp20-gcc-application"
    assert provenance["projection"]["overlay_fingerprint"].startswith("sha256:")
    assert provenance["projection"]["merge_decisions"] == []
    assert "POL-0001" in provenance["entries"]
    assert projection.entry == legacy.entry
    assert projection.principles == legacy.principles
    assert projection.topic_documents == legacy.topic_documents
    assert projection.standard_documents == legacy.standard_documents
    assert projection.exemplars == legacy.exemplars


def test_local_policy_joins_new_topic(tmp_path: Path) -> None:
    project = _project(tmp_path)
    policies = project.parent / "policies"
    _write(
        policies / "PRJ-POL-0001-local-frame.md",
        """---
id: PRJ-POL-0001
kind: guideline
trigger: encode a project frame
attribution:
  - source: project design
    locator: protocol
---

# Encode the project frame in network byte order
""",
    )
    _write(
        policies / "TOPICS.md",
        """# Local topics

## Topics

### Project networking

Read when: encoding the project's network protocol.

Review when: a change encodes or decodes the project's network protocol.

PRJ-POL-0001
""",
    )

    projection, _, _, _ = _build(project)

    assert "project-networking" in projection.topic_documents
    assert "PRJ-POL-0001" in projection.topic_documents["project-networking"]


def test_topic_exclusion_is_expanded_into_provenance(tmp_path: Path) -> None:
    project = _project(
        tmp_path,
        exclude_topics="[{topic: crossing-the-ffi-boundary, reason: no ABI boundary}]",
    )

    projection, _, _, _ = _build(project)

    provenance = json.loads(projection.sidecar)
    assert "crossing-the-ffi-boundary" not in projection.topic_documents
    decisions = provenance["projection"]["merge_decisions"]
    assert decisions[0] == {
        "operation": "exclude-topic",
        "target": "crossing-the-ffi-boundary",
        "reason": "no ABI boundary",
    }
    assert {
        "operation": "exclude-topic-member",
        "target": "POL-0026",
        "reason": "no ABI boundary",
    } in decisions
    assert "POL-0026" not in provenance["entries"]


def test_standard_replacement_preserves_audit_decision(tmp_path: Path) -> None:
    project = _project(
        tmp_path,
        replace_ids=(
            "[{upstream: STD-0029, local: PRJ-STD-0001, "
            "reason: existing suite uses GoogleTest}]"
        ),
    )
    _write(
        project.parent / "standard" / "PRJ-STD-0001-test-framework.md",
        """---
id: PRJ-STD-0001
group: toolchain
enforced_by: build
attribution:
  - source: project build
    locator: CMakeLists.txt
---

# The test framework is GoogleTest
""",
    )

    projection, _, _, _ = _build(project)

    provenance = json.loads(projection.sidecar)
    assert "STD-0029" not in provenance["entries"]
    assert "PRJ-STD-0001" in provenance["entries"]
    assert provenance["projection"]["merge_decisions"][0]["local"] == "PRJ-STD-0001"


def test_conflicting_exclusion_and_replacement_fails(tmp_path: Path) -> None:
    project = _project(
        tmp_path,
        exclude_ids="[{id: STD-0029, reason: not applicable}]",
        replace_ids=(
            "[{upstream: STD-0029, local: PRJ-STD-0001, "
            "reason: use project framework}]"
        ),
    )
    _write(
        project.parent / "standard" / "PRJ-STD-0001-test-framework.md",
        """---
id: PRJ-STD-0001
group: toolchain
enforced_by: build
attribution:
  - source: project build
    locator: CMakeLists.txt
---

# The test framework is GoogleTest
""",
    )

    with pytest.raises(PolcError, match="cannot be both excluded and replaced"):
        _build(project)


def test_reason_is_required_for_project_decisions(tmp_path: Path) -> None:
    project = _project(
        tmp_path,
        exclude_ids="[{id: POL-0001, reason: ''}]",
    )

    with pytest.raises(PolcError, match="'reason' must be a non-empty string"):
        load_project_configuration(project)


def test_replacement_of_inapplicable_upstream_id_fails(tmp_path: Path) -> None:
    project = _project(
        tmp_path,
        replace_ids=(
            "[{upstream: POL-0161, local: PRJ-POL-0001, "
            "reason: project-specific loop}]"
        ),
    )
    _write(
        project.parent / "policies" / "PRJ-POL-0001-loop.md",
        """---
id: PRJ-POL-0001
kind: guideline
trigger: run a project loop
attribution:
  - source: project design
    locator: loop
---

# Follow the project loop contract
""",
    )

    with pytest.raises(PolcError, match="POL-0161 is excluded by applicability"):
        _build(project)


def test_overlay_fingerprint_does_not_include_absolute_root(tmp_path: Path) -> None:
    first = _project(tmp_path / "first")
    second = _project(tmp_path / "second")
    _write(first.parent / "policies" / "note.txt", "same\n")
    _write(second.parent / "policies" / "note.txt", "same\n")

    assert overlay_fingerprint(first, first.parent) == overlay_fingerprint(
        second, second.parent
    )
