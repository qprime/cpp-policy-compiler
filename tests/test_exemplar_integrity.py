from __future__ import annotations

from pathlib import Path

REPOSITORY = Path(__file__).parents[1]
EXEMPLARS = REPOSITORY / "docs/exemplars"


def _copies(relative: str) -> list[Path]:
    return sorted(EXEMPLARS.glob(f"EXM-*/{relative}"))


def test_shared_temperature_evidence_is_identical_and_rejects_non_finite() -> None:
    sources = _copies("core/temperature.cpp")
    tests = _copies("core/temperature_test.cpp")

    assert len(sources) == len(tests) == 11
    assert len({path.read_bytes() for path in sources}) == 1
    assert len({path.read_bytes() for path in tests}) == 1
    assert "std::isfinite(celsius)" in sources[0].read_text(encoding="utf-8")
    assert "rejects_non_finite_values" in tests[0].read_text(encoding="utf-8")


def test_coroutine_task_disconnects_before_destroying_its_frame() -> None:
    root = EXEMPLARS / "EXM-0014-coroutine"
    source = (root / "device/async_read.cpp").read_text(encoding="utf-8")
    test = (root / "device/async_read_test.cpp").read_text(encoding="utf-8")

    destructor = source.index("ReadTask::~ReadTask()")
    cancel = source.index("cancel_wait();", destructor)
    destroy = source.index("handle_.destroy();", destructor)
    assert cancel < destroy
    assert "destroying_an_unfinished_task_disconnects_its_continuation" in test


def test_public_c_fixture_validates_pointer_arguments() -> None:
    source = (
        EXEMPLARS / "EXM-0013-ffi-boundary/ffi/driver_adapter_test.cpp"
    ).read_text(encoding="utf-8")

    assert "endpoint == nullptr || out_session == nullptr" in source
    assert "session == nullptr || out_celsius == nullptr" in source
    assert "the_public_c_boundary_rejects_invalid_pointers" in source
    assert "assert(" not in source
