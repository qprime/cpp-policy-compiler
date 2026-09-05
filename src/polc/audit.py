from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .corpus import load_corpus
from .exemplars import load_exemplars
from .manifest import parse_manifest
from .model import PolcError
from .standard import load_standard

SCHEMA_VERSION = 1
SLICE_PRINCIPLES = "principles-anti-patterns"
SLICE_TOPIC_NAMES = (
    "topics-01-05",
    "topics-06-10",
    "topics-11-15",
    "topics-16-20",
)
SLICE_STANDARD = "coding-standard"
SLICE_EXEMPLARS = "exemplars-integration"
SLICES = (SLICE_PRINCIPLES, *SLICE_TOPIC_NAMES, SLICE_STANDARD, SLICE_EXEMPLARS)
REPORTS = {name: f"reports/{name}.json" for name in SLICES}

DISPOSITIONS = {"keep", "revise", "split", "merge", "remove"}
SEVERITIES = {"blocking", "major", "minor", "note"}
DIMENSION_STATES = {"reviewed", "not-applicable", "finding"}
DIMENSIONS = (
    "technical_truth", "strength", "scope", "decision_clarity",
    "generation_routing", "review_routing", "consistency", "attribution",
    "examples_and_evidence", "model_behavior",
)


def _relative(path: Path, repository: Path) -> str:
    try:
        return path.resolve().relative_to(repository.resolve()).as_posix()
    except ValueError as exc:
        raise PolcError(
            [f"{path}: corpus path is outside repository root {repository}"]
        ) from exc


def build_inventory(
    repository: Path, policies_dir: Path, standard_dir: Path, exemplars_dir: Path
) -> dict[str, Any]:
    policies = load_corpus(policies_dir)
    topics = parse_manifest(policies_dir / "TOPICS.md")
    standards = load_standard(standard_dir)
    exemplars = load_exemplars(exemplars_dir)
    topic_by_id: dict[str, tuple[int, str]] = {}
    errors: list[str] = []
    for index, topic in enumerate(topics):
        for identity in topic.members:
            if identity in topic_by_id:
                errors.append(f"{identity}: duplicate topic membership")
            topic_by_id[identity] = (index, topic.name)

    items: list[dict[str, Any]] = []
    for policy in policies:
        topic_info = topic_by_id.get(policy.id)
        if policy.kind in {"principle", "anti-pattern"}:
            slice_name = SLICE_PRINCIPLES
        elif topic_info is None:
            errors.append(f"{policy.id}: no topic membership for audit ownership")
            continue
        else:
            topic_index, _ = topic_info
            if topic_index >= 20:
                errors.append(
                    f"{policy.id}: topic index {topic_index + 1} is outside audit slices"
                )
                continue
            slice_name = SLICE_TOPIC_NAMES[topic_index // 5]
        items.append({
            "id": policy.id,
            "kind": "policy",
            "policy_kind": policy.kind,
            "path": _relative(policy.path, repository),
            "topic": topic_info[1] if topic_info else None,
            "slice": slice_name,
        })
    for entry in standards:
        items.append({
            "id": entry.id, "kind": "standard",
            "path": _relative(entry.path, repository), "group": entry.group,
            "slice": SLICE_STANDARD,
        })
    for exemplar in exemplars:
        items.append({
            "id": exemplar.id, "kind": "exemplar",
            "path": _relative(exemplar.directory / "exemplar.md", repository),
            "slice": SLICE_EXEMPLARS,
        })
    if errors:
        raise PolcError(errors)
    kind_order = {"policy": 0, "standard": 1, "exemplar": 2}
    items.sort(key=lambda item: (kind_order[item["kind"]], item["id"]))
    return {"schema_version": SCHEMA_VERSION, "reports": REPORTS, "items": items}


def serialize_inventory(inventory: dict[str, Any]) -> str:
    return json.dumps(inventory, indent=2, ensure_ascii=False) + "\n"


def _load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        errors.append(f"{path}: cannot read: {exc}")
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
    return None


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _check_portability(value: Any, origin: str, errors: list[str]) -> None:
    for text in _strings(value):
        if text.startswith("/") or "\\" in text:
            errors.append(
                f"{origin}: absolute or non-portable path is forbidden: {text!r}"
            )
        if text.lower() in {"created_at", "updated_at", "timestamp"}:
            errors.append(f"{origin}: volatile timestamp field is forbidden: {text!r}")


def _validate_record(
    record: Any, origin: str, final: bool, errors: list[str]
) -> str | None:
    if not isinstance(record, dict):
        errors.append(f"{origin}: record must be an object")
        return None
    identity = record.get("id")
    if not isinstance(identity, str):
        errors.append(f"{origin}: record id must be a string")
        return None
    prefix = f"{origin}: {identity}"
    disposition = record.get("disposition")
    severity = record.get("highest_severity")
    if disposition not in DISPOSITIONS:
        errors.append(f"{prefix}: invalid or missing disposition {disposition!r}")
    if severity not in SEVERITIES:
        errors.append(f"{prefix}: invalid or missing highest_severity {severity!r}")
    if not isinstance(record.get("rationale"), str) or not record["rationale"].strip():
        errors.append(f"{prefix}: rationale must be non-empty")
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) for item in evidence):
        errors.append(f"{prefix}: evidence must be a non-empty list of strings")
    related = record.get("related_ids")
    if not isinstance(related, list) or not all(isinstance(item, str) for item in related):
        errors.append(f"{prefix}: related_ids must be a list of strings")
    dimensions = record.get("dimensions")
    if not isinstance(dimensions, dict):
        errors.append(f"{prefix}: dimensions must be an object")
    else:
        missing = sorted(set(DIMENSIONS) - dimensions.keys())
        unknown = sorted(dimensions.keys() - set(DIMENSIONS))
        if missing:
            errors.append(f"{prefix}: missing dimensions: {', '.join(missing)}")
        if unknown:
            errors.append(f"{prefix}: unknown dimensions: {', '.join(unknown)}")
        for name, result in dimensions.items():
            if not isinstance(result, dict) or result.get("status") not in DIMENSION_STATES:
                errors.append(f"{prefix}: dimension {name} has invalid or missing status")
            elif result["status"] in {"not-applicable", "finding"} and not result.get("reason"):
                errors.append(f"{prefix}: dimension {name} requires a reason")
    change = record.get("change")
    follow_up = record.get("follow_up_issue")
    if change is not None:
        if not isinstance(change, dict):
            errors.append(f"{prefix}: change must be null or an object")
        else:
            files, commit = change.get("files"), change.get("commit")
            if not isinstance(files, list) or not files or not all(isinstance(item, str) for item in files):
                errors.append(f"{prefix}: change.files must be a non-empty list of paths")
            if not isinstance(commit, str) or not commit.strip():
                errors.append(f"{prefix}: change.commit must be non-empty")
    if follow_up is not None and (not isinstance(follow_up, str) or not follow_up.strip()):
        errors.append(f"{prefix}: follow_up_issue must be null or a non-empty string")
    if disposition in DISPOSITIONS - {"keep"} and change is None and follow_up is None:
        errors.append(f"{prefix}: non-keep disposition requires change or follow_up_issue")
    finding_status = record.get("finding_status")
    if finding_status not in {"resolved", "unresolved"}:
        errors.append(f"{prefix}: finding_status must be resolved or unresolved")
    if final and finding_status == "unresolved" and severity in {"blocking", "major"}:
        errors.append(f"{prefix}: final audit has unresolved {severity} finding")
    return identity


def check(
    audit_root: Path, repository: Path, policies_dir: Path,
    standard_dir: Path, exemplars_dir: Path, *, final: bool = False,
) -> tuple[int, int, int]:
    errors: list[str] = []
    inventory_path = audit_root / "inventory.json"
    inventory = _load_json(inventory_path, errors)
    live = build_inventory(repository, policies_dir, standard_dir, exemplars_dir)
    if inventory is not None:
        _check_portability(inventory, str(inventory_path), errors)
        if serialize_inventory(inventory) != serialize_inventory(live):
            errors.append(f"{inventory_path}: inventory differs from the live corpus")
    owned = {name: [] for name in SLICES}
    for item in live["items"]:
        owned[item["slice"]].append(item["id"])
    seen: dict[str, str] = {}
    for slice_name in SLICES:
        report_path = audit_root / REPORTS[slice_name]
        report = _load_json(report_path, errors)
        if report is None:
            continue
        _check_portability(report, str(report_path), errors)
        if not isinstance(report, dict):
            errors.append(f"{report_path}: report must be an object")
            continue
        if report.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"{report_path}: schema_version must be {SCHEMA_VERSION}")
        if report.get("slice") != slice_name:
            errors.append(f"{report_path}: slice must be {slice_name!r}")
        status, records = report.get("status"), report.get("records")
        if status not in {"pending", "complete"}:
            errors.append(f"{report_path}: status must be pending or complete")
            continue
        if not isinstance(records, list):
            errors.append(f"{report_path}: records must be a list")
            continue
        if status == "pending":
            if records:
                errors.append(f"{report_path}: pending report must have no records")
            if final:
                errors.append(f"{report_path}: final audit cannot contain a pending slice")
            continue
        report_ids: list[str] = []
        for index, record in enumerate(records):
            identity = _validate_record(record, f"{report_path} record {index + 1}", final, errors)
            if identity is not None:
                report_ids.append(identity)
                if identity in seen:
                    errors.append(f"{identity}: appears in both {seen[identity]} and {slice_name}")
                else:
                    seen[identity] = slice_name
        if report_ids != owned[slice_name]:
            errors.append(f"{report_path}: record identities or order differ from inventory ownership")
    if errors:
        raise PolcError(errors)
    return tuple(
        sum(item["kind"] == kind for item in live["items"])
        for kind in ("policy", "standard", "exemplar")
    )  # type: ignore[return-value]
