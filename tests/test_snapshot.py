from __future__ import annotations

import json
import sys
from pathlib import Path

from polc.snapshot import record


def test_record_captures_original_quiet_and_final_states(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    root.mkdir()
    _write = root.joinpath("sample.cpp").write_text
    _write("original\n", encoding="utf-8")
    script = root / "change.py"
    script.write_text(
        """from pathlib import Path
import time

path = Path("sample.cpp")
path.write_text("first\\n", encoding="utf-8")
time.sleep(0.2)
path.write_text("final\\n", encoding="utf-8")
""",
        encoding="utf-8",
    )

    manifest = record(
        root,
        ("sample.cpp",),
        tmp_path / "recording",
        (sys.executable, "change.py"),
        quiet_period_ms=75,
        poll_period_ms=10,
    )

    assert manifest["exit_code"] == 0
    assert [state["label"] for state in manifest["timeline"]] == [
        "original",
        "quiet",
        "final",
    ]
    recorded = json.loads(
        (tmp_path / "recording" / "recording.json").read_text(encoding="utf-8")
    )
    assert recorded["final_digest"] == manifest["timeline"][-1]["digest"]


def test_record_stores_repeated_content_only_once(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    root.mkdir()
    (root / "sample.cpp").write_text("same\n", encoding="utf-8")
    script = root / "change.py"
    script.write_text(
        """from pathlib import Path
import time

path = Path("sample.cpp")
path.write_text("different\\n", encoding="utf-8")
time.sleep(0.15)
path.write_text("same\\n", encoding="utf-8")
""",
        encoding="utf-8",
    )

    manifest = record(
        root,
        ("sample.cpp",),
        tmp_path / "recording",
        (sys.executable, "change.py"),
        quiet_period_ms=50,
        poll_period_ms=10,
    )

    assert len(manifest["timeline"]) == 2
    assert manifest["final_digest"] == manifest["timeline"][0]["digest"]


def test_record_expands_a_watched_directory(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    source = root / "src"
    source.mkdir(parents=True)
    (source / "first.cpp").write_text("first\n", encoding="utf-8")
    script = root / "change.py"
    script.write_text(
        """from pathlib import Path

Path("src/second.cpp").write_text("second\\n", encoding="utf-8")
""",
        encoding="utf-8",
    )

    manifest = record(
        root,
        ("src",),
        tmp_path / "recording",
        (sys.executable, "change.py"),
        quiet_period_ms=50,
        poll_period_ms=10,
    )

    final = next(
        state
        for state in manifest["timeline"]
        if state["digest"] == manifest["final_digest"]
    )
    assert [item["path"] for item in final["files"]] == [
        "src/first.cpp",
        "src/second.cpp",
    ]
