from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from polc.audit import DIMENSIONS, REPORTS, build_inventory, check, serialize_inventory
from polc.model import PolcError

REPOSITORY = Path(__file__).parents[1]
POLICIES = REPOSITORY / "docs/policies"
STANDARD = REPOSITORY / "docs/standard"
EXEMPLARS = REPOSITORY / "docs/exemplars"
AUDIT = REPOSITORY / "audits/corpus-v1"


def _check(audit: Path = AUDIT, *, final: bool = False) -> tuple[int, int, int]:
    return check(audit, REPOSITORY, POLICIES, STANDARD, EXEMPLARS, final=final)


def _copy_audit(tmp_path: Path) -> Path:
    target = tmp_path / "audit"
    shutil.copytree(AUDIT, target)
    return target


def _record(identity: str) -> dict[str, object]:
    return {
        "id": identity,
        "disposition": "keep",
        "dimensions": {name: {"status": "reviewed"} for name in DIMENSIONS},
        "highest_severity": "note",
        "rationale": "Reviewed affirmatively.",
        "evidence": ["docs/source/README.md"],
        "related_ids": [],
        "change": None,
        "follow_up_issue": None,
        "finding_status": "resolved",
    }


def _complete_slice(audit: Path, slice_name: str) -> Path:
    inventory = json.loads((audit / "inventory.json").read_text(encoding="utf-8"))
    records = [
        _record(item["id"])
        for item in inventory["items"]
        if item["slice"] == slice_name
    ]
    path = audit / REPORTS[slice_name]
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "slice": slice_name,
                "status": "complete",
                "records": records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def test_current_inventory_is_complete_unique_and_deterministic() -> None:
    first = build_inventory(REPOSITORY, POLICIES, STANDARD, EXEMPLARS)
    second = build_inventory(REPOSITORY, POLICIES, STANDARD, EXEMPLARS)
    assert serialize_inventory(first) == serialize_inventory(second)
    assert _check() == (247, 29, 14)
    identities = [item["id"] for item in first["items"]]
    assert len(identities) == len(set(identities)) == 290
    assert all(not Path(item["path"]).is_absolute() for item in first["items"])


def test_live_corpus_path_change_makes_inventory_stale(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    shutil.copytree(REPOSITORY / "docs", repository / "docs")
    shutil.copytree(AUDIT, repository / "audit")
    policy = next((repository / "docs/policies").glob("POL-*.md"))
    policy.rename(policy.with_name(policy.stem + "-renamed.md"))
    with pytest.raises(PolcError, match="inventory differs from the live corpus"):
        check(
            repository / "audit", repository, repository / "docs/policies",
            repository / "docs/standard", repository / "docs/exemplars",
        )


def test_incremental_accepts_pending_but_final_rejects_it() -> None:
    _check()
    with pytest.raises(PolcError, match="final audit cannot contain a pending slice"):
        _check(final=True)


def test_completed_report_requires_exact_owned_identity_order(tmp_path: Path) -> None:
    audit = _copy_audit(tmp_path)
    report_path = _complete_slice(audit, "principles-anti-patterns")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["records"].append(report["records"][0])
    report_path.write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(PolcError, match="appears in both|record identities or order differ"):
        _check(audit)


def test_completed_report_rejects_missing_fields_and_vocabulary(tmp_path: Path) -> None:
    audit = _copy_audit(tmp_path)
    report_path = _complete_slice(audit, "principles-anti-patterns")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["records"][0]["disposition"] = "approve"
    del report["records"][0]["dimensions"]["technical_truth"]
    report_path.write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(PolcError) as caught:
        _check(audit)
    assert "invalid or missing disposition" in str(caught.value)
    assert "missing dimensions: technical_truth" in str(caught.value)


def test_non_keep_requires_change_or_follow_up(tmp_path: Path) -> None:
    audit = _copy_audit(tmp_path)
    report_path = _complete_slice(audit, "principles-anti-patterns")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["records"][0]["disposition"] = "revise"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(PolcError, match="requires change or follow_up_issue"):
        _check(audit)


def test_final_rejects_unresolved_major_finding(tmp_path: Path) -> None:
    audit = _copy_audit(tmp_path)
    for slice_name in REPORTS:
        _complete_slice(audit, slice_name)
    report_path = audit / REPORTS["principles-anti-patterns"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["records"][0]["highest_severity"] = "major"
    report["records"][0]["finding_status"] = "unresolved"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(PolcError, match="final audit has unresolved major finding"):
        _check(audit, final=True)


def test_absolute_paths_and_timestamp_fields_are_rejected(tmp_path: Path) -> None:
    audit = _copy_audit(tmp_path)
    inventory_path = audit / "inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory["timestamp"] = "2026-01-01T00:00:00Z"
    inventory["items"][0]["path"] = "/tmp/policy.md"
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    with pytest.raises(PolcError) as caught:
        _check(audit)
    assert "volatile timestamp field" in str(caught.value)
    assert "absolute or non-portable path" in str(caught.value)
