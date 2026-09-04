from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

from .model import PolcError

CHECK_KINDS = ("contains", "not-contains", "command", "manual")


@dataclass(frozen=True)
class Requirement:
    id: str
    severity: str
    check: str
    path: str | None = None
    pattern: str | None = None
    command: tuple[str, ...] = ()


@dataclass(frozen=True)
class State:
    label: str
    root: Path


@dataclass(frozen=True)
class Variant:
    name: str
    states: tuple[State, ...] = ()
    findings: Path | None = None


@dataclass(frozen=True)
class ExpectedFinding:
    id: str
    path: str
    line: int
    line_end: int
    evidence: str


@dataclass(frozen=True)
class Benchmark:
    name: str
    kind: str
    source: str
    model: str | None
    observed_at: str | None
    prompt: str
    watched_paths: tuple[str, ...]
    requirements: tuple[Requirement, ...]
    variants: tuple[Variant, ...]
    expected_findings: tuple[ExpectedFinding, ...] = ()


def _mapping(value: object, origin: str, errors: list[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        errors.append(f"{origin}: expected a mapping")
        return {}
    return value


def _text(value: object, origin: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value:
        errors.append(f"{origin}: expected a non-empty string")
        return ""
    return value


def _items(value: object, origin: str, errors: list[str]) -> list[object]:
    if not isinstance(value, list):
        errors.append(f"{origin}: expected a list")
        return []
    return value


def _load_requirement(value: object, index: int, errors: list[str]) -> Requirement:
    origin = f"requirements[{index}]"
    item = _mapping(value, origin, errors)
    command_value = item.get("command", [])
    command = tuple(
        _text(part, f"{origin}.command", errors)
        for part in _items(command_value, f"{origin}.command", errors)
    )
    return Requirement(
        id=_text(item.get("id"), f"{origin}.id", errors),
        severity=_text(item.get("severity"), f"{origin}.severity", errors),
        check=_text(item.get("check"), f"{origin}.check", errors),
        path=item.get("path") if isinstance(item.get("path"), str) else None,
        pattern=item.get("pattern") if isinstance(item.get("pattern"), str) else None,
        command=command,
    )


def _load_state(
    value: object, index: int, base: Path, origin: str, errors: list[str]
) -> State:
    item = _mapping(value, f"{origin}.states[{index}]", errors)
    root = _text(item.get("root"), f"{origin}.states[{index}].root", errors)
    return State(
        label=_text(item.get("label"), f"{origin}.states[{index}].label", errors),
        root=base / root,
    )


def _load_variant(
    value: object, index: int, base: Path, errors: list[str]
) -> Variant:
    origin = f"variants[{index}]"
    item = _mapping(value, origin, errors)
    states = tuple(
        _load_state(state, state_index, base, origin, errors)
        for state_index, state in enumerate(
            _items(item.get("states", []), f"{origin}.states", errors)
        )
    )
    findings_value = item.get("findings")
    findings = base / findings_value if isinstance(findings_value, str) else None
    return Variant(
        name=_text(item.get("name"), f"{origin}.name", errors),
        states=states,
        findings=findings,
    )


def _load_expected_finding(
    value: object, index: int, errors: list[str]
) -> ExpectedFinding:
    origin = f"expected_findings[{index}]"
    item = _mapping(value, origin, errors)
    line = item.get("line")
    if isinstance(line, bool) or not isinstance(line, int) or line < 1:
        errors.append(f"{origin}.line: expected a positive integer")
        line = 0
    line_end = item.get("line_end", line)
    if (
        isinstance(line_end, bool)
        or not isinstance(line_end, int)
        or line_end < line
    ):
        errors.append(f"{origin}.line_end: expected an integer at or after line")
        line_end = line
    return ExpectedFinding(
        id=_text(item.get("id"), f"{origin}.id", errors),
        path=_text(item.get("path"), f"{origin}.path", errors),
        line=line,
        line_end=line_end,
        evidence=_text(item.get("evidence"), f"{origin}.evidence", errors),
    )


def load_benchmark(path: Path) -> Benchmark:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise PolcError([f"{path}: cannot read benchmark: {exc}"]) from exc
    except yaml.YAMLError as exc:
        raise PolcError([f"{path}: invalid YAML: {exc}"]) from exc
    errors: list[str] = []
    root = _mapping(data, path.name, errors)
    version = root.get("version")
    if version != 1:
        errors.append(f"{path.name}: version must be 1")
    kind = _text(root.get("kind"), "kind", errors)
    name = _text(root.get("name"), "name", errors)
    source = _text(root.get("source", "controlled-fixture"), "source", errors)
    model_value = root.get("model")
    if model_value is not None and not isinstance(model_value, str):
        errors.append("model: expected a string")
    observed_at_value = root.get("observed_at")
    if observed_at_value is not None and not isinstance(observed_at_value, str):
        errors.append("observed_at: expected a string")
    prompt = _text(root.get("prompt"), "prompt", errors)
    watched_paths = tuple(
        _text(value, "watched_paths", errors)
        for value in _items(root.get("watched_paths"), "watched_paths", errors)
    )
    if kind not in ("generation", "review"):
        errors.append("kind: expected 'generation' or 'review'")
    requirements = tuple(
        _load_requirement(value, index, errors)
        for index, value in enumerate(
            _items(root.get("requirements", []), "requirements", errors)
        )
    )
    variants = tuple(
        _load_variant(value, index, path.parent, errors)
        for index, value in enumerate(
            _items(root.get("variants"), "variants", errors)
        )
    )
    expected = tuple(
        _load_expected_finding(value, index, errors)
        for index, value in enumerate(
            _items(root.get("expected_findings", []), "expected_findings", errors)
        )
    )
    for requirement in requirements:
        if requirement.check not in CHECK_KINDS:
            errors.append(
                f"{requirement.id}: check must be one of {', '.join(CHECK_KINDS)}"
            )
        if requirement.check in ("contains", "not-contains") and (
            requirement.path is None or requirement.pattern is None
        ):
            errors.append(f"{requirement.id}: text checks require path and pattern")
        if requirement.check == "command" and not requirement.command:
            errors.append(f"{requirement.id}: command check requires command")
    if kind == "generation":
        for variant in variants:
            if len(variant.states) < 2:
                errors.append(
                    f"variant '{variant.name}': generation requires at least two states"
                )
    if kind == "review":
        if not expected:
            errors.append("review benchmark requires expected_findings")
        for variant in variants:
            if variant.findings is None:
                errors.append(f"variant '{variant.name}': review requires findings")
    if errors:
        raise PolcError([f"{path}: {error}" for error in errors])
    return Benchmark(
        name=name,
        kind=kind,
        source=source,
        model=model_value if isinstance(model_value, str) else None,
        observed_at=(
            observed_at_value
            if isinstance(observed_at_value, str)
            else None
        ),
        prompt=prompt,
        watched_paths=watched_paths,
        requirements=requirements,
        variants=variants,
        expected_findings=expected,
    )


def _evaluate_requirement(requirement: Requirement, root: Path) -> dict[str, object]:
    if requirement.check == "manual":
        return {
            "id": requirement.id,
            "severity": requirement.severity,
            "status": "not-judged",
            "evidence": "manual adjudication required",
        }
    if requirement.check == "command":
        try:
            completed = subprocess.run(
                requirement.command,
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as exc:
            return {
                "id": requirement.id,
                "severity": requirement.severity,
                "status": "error",
                "evidence": str(exc),
            }
        output = (completed.stdout + completed.stderr).strip()
        return {
            "id": requirement.id,
            "severity": requirement.severity,
            "status": "pass" if completed.returncode == 0 else "violation",
            "evidence": output,
        }
    target = root / (requirement.path or "")
    try:
        content = target.read_text(encoding="utf-8")
    except OSError as exc:
        return {
            "id": requirement.id,
            "severity": requirement.severity,
            "status": "error",
            "evidence": str(exc),
        }
    try:
        found = re.search(requirement.pattern or "", content, re.MULTILINE) is not None
    except re.error as exc:
        return {
            "id": requirement.id,
            "severity": requirement.severity,
            "status": "error",
            "evidence": f"invalid pattern: {exc}",
        }
    passed = found if requirement.check == "contains" else not found
    return {
        "id": requirement.id,
        "severity": requirement.severity,
        "status": "pass" if passed else "violation",
        "evidence": f"{requirement.path}: pattern {requirement.pattern!r} "
        f"{'found' if found else 'not found'}",
    }


def _generation_result(benchmark: Benchmark) -> dict[str, object]:
    variants = []
    for variant in benchmark.variants:
        states = []
        for state in variant.states:
            results = [
                _evaluate_requirement(requirement, state.root)
                for requirement in benchmark.requirements
            ]
            judged = [
                result
                for result in results
                if result["status"] in ("pass", "violation")
            ]
            states.append(
                {
                    "label": state.label,
                    "requirements": results,
                    "judged": len(judged),
                    "passed": sum(result["status"] == "pass" for result in judged),
                    "violations": sum(
                        result["status"] == "violation" for result in judged
                    ),
                }
            )
        first = states[1]
        final = states[-1]
        variants.append(
            {
                "name": variant.name,
                "states": states,
                "first_write_compliance": (
                    first["passed"] / first["judged"] if first["judged"] else None
                ),
                "final_compliance": (
                    final["passed"] / final["judged"] if final["judged"] else None
                ),
                "repair_delta": first["violations"] - final["violations"],
            }
        )
    return _result_header(benchmark) | {"variants": variants}


def _load_findings(path: Path) -> list[dict[str, object]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolcError([f"{path}: cannot load findings: {exc}"]) from exc
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise PolcError([f"{path}: findings must be a JSON list of objects"])
    errors: list[str] = []
    seen: set[tuple[str, str, int]] = set()
    for index, item in enumerate(data):
        finding_id = item.get("id")
        finding_path = item.get("path")
        line = item.get("line")
        evidence = item.get("evidence")
        if not isinstance(finding_id, str) or not finding_id:
            errors.append(f"finding[{index}].id must be a non-empty string")
        if not isinstance(finding_path, str) or not finding_path:
            errors.append(f"finding[{index}].path must be a non-empty string")
        if isinstance(line, bool) or not isinstance(line, int) or line < 1:
            errors.append(f"finding[{index}].line must be a positive integer")
        if not isinstance(evidence, str):
            errors.append(f"finding[{index}].evidence must be a string")
        if (
            isinstance(finding_id, str)
            and isinstance(finding_path, str)
            and isinstance(line, int)
        ):
            key = (finding_id, finding_path, line)
            if key in seen:
                errors.append(
                    f"finding[{index}] duplicates {finding_id}|{finding_path}|{line}"
                )
            seen.add(key)
    if errors:
        raise PolcError([f"{path}: {error}" for error in errors])
    return data


def _review_result(benchmark: Benchmark) -> dict[str, object]:
    variants = []
    for variant in benchmark.variants:
        findings = _load_findings(variant.findings or Path())
        unmatched = list(benchmark.expected_findings)
        matches: list[tuple[ExpectedFinding, dict[str, object]]] = []
        unsupported: list[dict[str, object]] = []
        for finding in findings:
            match = next(
                (
                    item
                    for item in unmatched
                    if finding["path"] == item.path
                    and item.line <= finding["line"] <= item.line_end
                ),
                None,
            )
            if match is None:
                unsupported.append(finding)
                continue
            unmatched.remove(match)
            matches.append((match, finding))
        actionable = [
            finding
            for _, finding in matches
            if isinstance(finding["evidence"], str) and bool(finding["evidence"].strip())
        ]
        cited = [finding for item, finding in matches if finding["id"] == item.id]
        variants.append(
            {
                "name": variant.name,
                "expected": len(benchmark.expected_findings),
                "reported": len(findings),
                "found": len(matches),
                "actionable": len(actionable),
                "missed": [
                    f"{item.id}|{item.path}|{item.line}"
                    for item in sorted(
                        unmatched, key=lambda item: (item.id, item.path, item.line)
                    )
                ],
                "unsupported": [
                    f"{item['id']}|{item['path']}|{item['line']}"
                    for item in sorted(
                        unsupported,
                        key=lambda item: (
                            str(item["id"]),
                            str(item["path"]),
                            int(item["line"]),
                        ),
                    )
                ],
                "review_recall": len(matches) / len(benchmark.expected_findings),
                "review_precision": len(matches) / len(findings) if findings else None,
                "citation_accuracy": len(cited) / len(matches) if matches else None,
                "actionability": len(actionable) / len(matches) if matches else None,
            }
        )
    return _result_header(benchmark) | {"variants": variants}


def _result_header(benchmark: Benchmark) -> dict[str, object]:
    return {
        "name": benchmark.name,
        "kind": benchmark.kind,
        "source": benchmark.source,
        "model": benchmark.model,
        "observed_at": benchmark.observed_at,
        "prompt": benchmark.prompt,
        "watched_paths": list(benchmark.watched_paths),
    }


def evaluate(path: Path) -> dict[str, object]:
    benchmark = load_benchmark(path)
    if benchmark.kind == "generation":
        return _generation_result(benchmark)
    return _review_result(benchmark)


def write_result(result: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
