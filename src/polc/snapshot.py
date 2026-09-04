from __future__ import annotations

import hashlib
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from .model import PolcError


@dataclass(frozen=True)
class ObservedFile:
    path: str
    digest: str | None


def _digest(path: Path) -> str | None:
    try:
        content = path.read_bytes()
    except FileNotFoundError:
        return None
    return hashlib.sha256(content).hexdigest()


def _observed_paths(root: Path, watched: tuple[str, ...]) -> tuple[str, ...]:
    paths: set[str] = set()
    for selector in watched:
        candidate = root / selector
        if candidate.is_dir():
            paths.update(
                path.relative_to(root).as_posix()
                for path in candidate.rglob("*")
                if path.is_file()
            )
        else:
            paths.add(selector)
    return tuple(sorted(paths))


def _state(root: Path, watched: tuple[str, ...]) -> tuple[ObservedFile, ...]:
    return tuple(
        ObservedFile(path, _digest(root / path))
        for path in _observed_paths(root, watched)
    )


def _save_state(
    root: Path,
    out: Path,
    state: tuple[ObservedFile, ...],
    label: str,
    started: float,
    timeline: list[dict[str, object]],
    seen: set[str],
) -> None:
    state_key = "\n".join(f"{item.path}:{item.digest}" for item in state)
    digest = hashlib.sha256(state_key.encode()).hexdigest()
    if digest in seen:
        return
    state_dir = out / "states" / f"{len(timeline):04d}-{digest[:12]}"
    files = []
    for item in state:
        if item.digest is None:
            files.append({"path": item.path, "digest": None})
            continue
        destination = state_dir / item.path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((root / item.path).read_bytes())
        files.append({"path": item.path, "digest": item.digest})
    timeline.append(
        {
            "label": label,
            "elapsed_ms": round((time.monotonic() - started) * 1000),
            "digest": digest,
            "root": str(state_dir.relative_to(out)),
            "files": files,
        }
    )
    seen.add(digest)


def record(
    root: Path,
    watched: tuple[str, ...],
    out: Path,
    command: tuple[str, ...],
    quiet_period_ms: int,
    poll_period_ms: int = 50,
) -> dict[str, object]:
    if quiet_period_ms < 1 or poll_period_ms < 1:
        raise PolcError(["quiet and poll periods must be positive"])
    if not command:
        raise PolcError(["record requires a command to observe"])
    for path in watched:
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise PolcError([f"watched path must stay below root: {path}"])
    out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    timeline: list[dict[str, object]] = []
    seen: set[str] = set()
    current = _state(root, watched)
    _save_state(root, out, current, "original", started, timeline, seen)
    try:
        process = subprocess.Popen(command, cwd=root)
    except OSError as exc:
        raise PolcError([f"cannot start observed command: {exc}"]) from exc
    changed_at = time.monotonic()
    pending = False
    while process.poll() is None:
        observed = _state(root, watched)
        if observed != current:
            current = observed
            changed_at = time.monotonic()
            pending = True
        if pending and (time.monotonic() - changed_at) * 1000 >= quiet_period_ms:
            _save_state(root, out, current, "quiet", started, timeline, seen)
            pending = False
        time.sleep(poll_period_ms / 1000)
    final = _state(root, watched)
    _save_state(root, out, final, "final", started, timeline, seen)
    final_key = "\n".join(f"{item.path}:{item.digest}" for item in final)
    final_digest = hashlib.sha256(final_key.encode()).hexdigest()
    manifest = {
        "version": 1,
        "root": str(root.resolve()),
        "command": list(command),
        "quiet_period_ms": quiet_period_ms,
        "exit_code": process.returncode,
        "final_digest": final_digest,
        "timeline": timeline,
    }
    (out / "recording.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest
