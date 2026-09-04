from __future__ import annotations

import json
from pathlib import Path

import pytest

from polc.evaluation import evaluate, load_benchmark
from polc.model import PolcError


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_generation_distinguishes_first_write_from_repair(tmp_path: Path) -> None:
    _write(tmp_path / "first" / "sample.cpp", "return std::move(result);\n")
    _write(tmp_path / "final" / "sample.cpp", "return result;\n")
    _write(
        tmp_path / "benchmark.yaml",
        """version: 1
name: return-shape
kind: generation
prompt: implement the return shapes
watched_paths: [sample.cpp]
requirements:
  - id: POL-0049
    severity: correctness
    check: not-contains
    path: sample.cpp
    pattern: 'std::move'
variants:
  - name: baseline
    states:
      - {label: T0, root: first}
      - {label: T1, root: first}
      - {label: final, root: final}
""",
    )

    result = evaluate(tmp_path / "benchmark.yaml")

    variant = result["variants"][0]
    assert variant["first_write_compliance"] == 0.0
    assert variant["final_compliance"] == 1.0
    assert variant["repair_delta"] == 1


def test_review_reports_recall_precision_and_false_positive(tmp_path: Path) -> None:
    _write(
        tmp_path / "findings.json",
        json.dumps(
            [
                {
                    "id": "POL-0049",
                    "path": "sample.cpp",
                    "line": 4,
                    "evidence": "return std::move(result)",
                },
                {
                    "id": "POL-9999",
                    "path": "sample.cpp",
                    "line": 8,
                    "evidence": "unsupported",
                },
            ]
        ),
    )
    _write(
        tmp_path / "benchmark.yaml",
        """version: 1
name: review-return-shape
kind: review
prompt: review sample.cpp
watched_paths: [sample.cpp]
requirements: []
expected_findings:
  - id: POL-0049
    path: sample.cpp
    line: 4
    evidence: return moves a local
  - id: POL-0137
    path: sample.cpp
    line: 6
    evidence: zero used as null
variants:
  - name: baseline
    findings: findings.json
""",
    )

    result = evaluate(tmp_path / "benchmark.yaml")

    variant = result["variants"][0]
    assert variant["review_recall"] == 0.5
    assert variant["review_precision"] == 0.5
    assert variant["citation_accuracy"] == 1.0
    assert variant["actionability"] == 1.0
    assert variant["missed"] == ["POL-0137|sample.cpp|6"]
    assert variant["unsupported"] == ["POL-9999|sample.cpp|8"]


def test_unknown_check_fails_at_manifest_boundary(tmp_path: Path) -> None:
    _write(
        tmp_path / "benchmark.yaml",
        """version: 1
name: bad-check
kind: generation
prompt: implement the return shape
watched_paths: [sample.cpp]
requirements:
  - id: POL-0049
    severity: correctness
    check: intuition
variants:
  - name: baseline
    states:
      - {label: T0, root: .}
      - {label: T1, root: .}
""",
    )

    with pytest.raises(PolcError, match="check must be one of"):
        load_benchmark(tmp_path / "benchmark.yaml")


def test_command_check_runs_inside_each_state(tmp_path: Path) -> None:
    _write(tmp_path / "state" / "present.txt", "yes\n")
    _write(
        tmp_path / "benchmark.yaml",
        """version: 1
name: command-check
kind: generation
prompt: inspect the state
watched_paths: [present.txt]
requirements:
  - id: BUILD
    severity: hard
    check: command
    command:
      - python3
      - -c
      - "from pathlib import Path; raise SystemExit(not Path('present.txt').is_file())"
variants:
  - name: baseline
    states:
      - {label: T0, root: state}
      - {label: T1, root: state}
""",
    )

    result = evaluate(tmp_path / "benchmark.yaml")

    assert result["variants"][0]["first_write_compliance"] == 1.0
