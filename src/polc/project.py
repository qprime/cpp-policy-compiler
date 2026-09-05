from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import dataclass, replace
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from . import adapters
from .corpus import fingerprint
from .model import Exemplar, PolcError, ProjectionMode
from .render import Projection, write
from .resources import (
    LOCK_SCHEMA_VERSION,
    PROJECT_LAYOUT_VERSION,
    PROJECTION_FORMAT_VERSION,
)

LOCK_VERSION = LOCK_SCHEMA_VERSION
CONTEXT = {
    "layers.md": (
        "# Layers\n\nDescribe the project's layers, allowed dependencies, and failure "
        "boundaries here.\n"
    ),
    "invariants.md": (
        "# Invariants\n\nDescribe the project's load-bearing subsystem invariants here.\n"
    ),
}


@dataclass(frozen=True)
class Inputs:
    root: Path
    policies: Path
    standard: Path
    exemplars: Path


def _polc_version() -> str:
    try:
        return version("polc")
    except PackageNotFoundError as exc:
        raise PolcError(["distribution 'polc' is not installed"]) from exc


def _paths(adapter: str | None) -> dict[ProjectionMode, Path]:
    return adapters.destinations(adapter)


def _lock(inputs: Inputs, adapter: str | None) -> dict[str, object]:
    paths = _paths(adapter)
    return {
        "version": LOCK_VERSION,
        "projection_format_version": PROJECTION_FORMAT_VERSION,
        "polc_version": _polc_version(),
        "corpus_fingerprint": fingerprint(
            inputs.policies, inputs.standard, inputs.exemplars
        ),
        "adapter": adapter,
        "destinations": {mode.value: paths[mode].as_posix() for mode in paths},
    }


def _read_lock(
    root: Path, allow_projection_mismatch: bool = False
) -> dict[str, object]:
    path = root / ".polc/lock.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolcError([f"{path}: cannot read a valid project lock: {exc}"]) from exc
    legacy = {
        "version",
        "polc_version",
        "corpus_fingerprint",
        "adapter",
        "destinations",
    }
    required = legacy | {
        "projection_format_version",
    }
    if isinstance(data, dict) and data.get("version") == 1:
        if set(data) != legacy:
            raise PolcError([f"{path}: invalid version 1 lock structure"])
        if not allow_projection_mismatch:
            raise PolcError(
                [
                    f"{path}: lock schema 1 is incompatible with executing schema "
                    f"{LOCK_VERSION}; run project diff then project accept"
                ]
            )
        data = {
            **data,
            "version": LOCK_VERSION,
            "projection_format_version": 0,
        }
    if not isinstance(data, dict) or set(data) != required:
        raise PolcError(
            [f"{path}: lock must contain exactly {', '.join(sorted(required))}"]
        )
    if data["version"] != LOCK_VERSION:
        raise PolcError(
            [
                f"{path}: lock schema {data['version']!r} is incompatible with "
                f"executing schema {LOCK_VERSION}"
            ]
        )
    if (
        data["projection_format_version"] != PROJECTION_FORMAT_VERSION
        and not allow_projection_mismatch
    ):
        raise PolcError(
            [
                f"{path}: projection format {data['projection_format_version']!r} "
                f"is incompatible with executing format {PROJECTION_FORMAT_VERSION}"
            ]
        )
    adapter = data["adapter"]
    if adapter is not None and adapter not in adapters.ADAPTERS:
        raise PolcError([f"{path}: unknown locked adapter {adapter!r}"])
    expected = {m.value: p.as_posix() for m, p in _paths(adapter).items()}
    if data["destinations"] != expected:
        raise PolcError([f"{path}: destinations do not match adapter layout"])
    return data


def _context(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in CONTEXT:
        path = root / ".polc/context" / name
        try:
            result[name] = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise PolcError([f"{path}: cannot read project context: {exc}"]) from exc
    return result


def _managed(projection: Projection, adapter: str | None) -> Projection:
    sidecar = json.loads(projection.sidecar)
    sidecar["projection"]["managed"] = True
    sidecar["projection"]["layout_version"] = PROJECT_LAYOUT_VERSION
    sidecar["projection"]["adapter"] = adapter
    return replace(projection, sidecar=json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n")


def _build_pair(
    inputs: Inputs, adapter: str | None
) -> dict[ProjectionMode, tuple[Projection, list[Exemplar]]]:
    # Imported lazily to keep the repository-author builder usable on its own.
    from .cli import _build_project_projection

    context = _context(inputs.root)
    pair: dict[ProjectionMode, tuple[Projection, list[Exemplar]]] = {}
    for mode in ProjectionMode:
        projection, _, _, exemplars = _build_project_projection(
            inputs.root / ".polc/project.md",
            inputs.policies,
            inputs.standard,
            inputs.exemplars,
            adapter,
            mode,
            context,
        )
        pair[mode] = (_managed(projection, adapter), exemplars)
    return pair


def _assert_owned(path: Path, mode: ProjectionMode, adapter: str | None) -> None:
    if not path.exists():
        return
    provenance = path / "provenance.json"
    try:
        projection = json.loads(provenance.read_text(encoding="utf-8"))["projection"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise PolcError([f"{path}: refusing to replace an unowned output directory"]) from exc
    if not (
        projection.get("managed") is True
        and projection.get("layout_version") == PROJECT_LAYOUT_VERSION
        and projection.get("mode") == mode.value
        and projection.get("adapter") == adapter
    ):
        raise PolcError([f"{path}: provenance does not prove expected project ownership"])


def _files(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _stage_pair(
    pair: dict[ProjectionMode, tuple[Projection, list[Exemplar]]], stage: Path, adapter: str | None
) -> dict[ProjectionMode, Path]:
    staged: dict[ProjectionMode, Path] = {}
    for mode, (projection, exemplars) in pair.items():
        destination = stage / mode.value
        write(projection, exemplars, destination)
        staged[mode] = destination
    return staged


def _install(replacements: list[tuple[Path | None, Path]], work: Path) -> None:
    backups: list[tuple[Path, Path]] = []
    installed: list[Path] = []
    try:
        for index, (source, destination) in enumerate(replacements):
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                backup = work / f"backup-{index}"
                destination.replace(backup)
                backups.append((backup, destination))
            if source is not None:
                source.replace(destination)
                installed.append(destination)
    except BaseException as exc:
        for destination in reversed(installed):
            if destination.is_dir():
                shutil.rmtree(destination)
            elif destination.exists():
                destination.unlink()
        for backup, destination in reversed(backups):
            backup.replace(destination)
        if isinstance(exc, OSError):
            raise PolcError(
                [f"project update failed and was rolled back: {exc}"]
            ) from exc
        raise


def _verify_release(inputs: Inputs, lock: dict[str, object]) -> None:
    candidate = _lock(inputs, lock["adapter"])
    for key in ("polc_version", "corpus_fingerprint"):
        if lock[key] != candidate[key]:
            raise PolcError(
                [
                    f"locked {key} is {lock[key]!r}, executing release is "
                    f"{candidate[key]!r}; run project diff then project accept"
                ]
            )


def init(
    inputs: Inputs,
    name: str,
    language_version: int,
    compiler: str,
    domain: str,
    adapter: str | None,
) -> list[str]:
    root = inputs.root.resolve()
    inputs = replace(inputs, root=root)
    if (root / ".polc").exists():
        raise PolcError([f"{root / '.polc'}: refusing to overwrite existing project inputs"])
    paths = _paths(adapter)
    for mode, relative in paths.items():
        _assert_owned(root / relative, mode, adapter)
        if (root / relative).exists():
            raise PolcError([f"{root / relative}: refusing to adopt an existing output"])
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".polc-init-", dir=root) as temp:
        work = Path(temp)
        staged_polc = work / ".polc"
        for directory in ("policies", "standard", "exemplars", "context"):
            (staged_polc / directory).mkdir(parents=True)
        project = (
            "---\n"
            f"name: {json.dumps(name)}\nlanguage_version: {language_version}\n"
            f"compiler: {json.dumps(compiler)}\ndomain: {json.dumps(domain)}\n"
            "exclude_topics: []\nexclude_ids: []\nreplace_ids: []\n---\n\n"
            "# Project policy overlay\n"
        )
        (staged_polc / "project.md").write_text(project, encoding="utf-8")
        for filename, text in CONTEXT.items():
            (staged_polc / "context" / filename).write_text(text, encoding="utf-8")
        lock = _lock(inputs, adapter)
        (staged_polc / "lock.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
        staged_inputs = replace(inputs, root=work)
        pair = _build_pair(staged_inputs, adapter)
        staged = _stage_pair(pair, work / "outputs", adapter)
        replacements = [(staged_polc, root / ".polc")]
        replacements.extend((staged[mode], root / relative) for mode, relative in paths.items())
        _install(replacements, work)
    return [
        note
        for mode, relative in paths.items()
        if (note := adapters.wiring_note(adapter, relative, pair[mode][0]))
    ]


def check(inputs: Inputs) -> list[str]:
    lock = _read_lock(inputs.root)
    _verify_release(inputs, lock)
    adapter = lock["adapter"]
    paths = _paths(adapter)
    pair = _build_pair(inputs, adapter)
    drift: list[str] = []
    with tempfile.TemporaryDirectory(prefix="polc-check-") as temp:
        staged = _stage_pair(pair, Path(temp), adapter)
        for mode, relative in paths.items():
            actual = inputs.root / relative
            _assert_owned(actual, mode, adapter)
            expected_files, actual_files = _files(staged[mode]), _files(actual)
            for name in sorted(expected_files.keys() | actual_files.keys()):
                if expected_files.get(name) != actual_files.get(name):
                    drift.append(f"{relative}/{name}")
    if drift:
        raise PolcError(["generated output drift: " + ", ".join(drift)])
    return ["generation and review outputs are current"]


def build(inputs: Inputs) -> list[str]:
    lock = _read_lock(inputs.root)
    _verify_release(inputs, lock)
    adapter = lock["adapter"]
    paths = _paths(adapter)
    for mode, relative in paths.items():
        _assert_owned(inputs.root / relative, mode, adapter)
    with tempfile.TemporaryDirectory(prefix=".polc-build-", dir=inputs.root) as temp:
        work = Path(temp)
        staged = _stage_pair(_build_pair(inputs, adapter), work / "outputs", adapter)
        _install([(staged[m], inputs.root / p) for m, p in paths.items()], work)
    return ["rebuilt generation and review outputs"]


def diff(inputs: Inputs) -> list[str]:
    lock = _read_lock(inputs.root, allow_projection_mismatch=True)
    adapter = lock["adapter"]
    candidate = _lock(inputs, adapter)
    lines = [
        f"polc: {lock['polc_version']} -> {candidate['polc_version']}",
        f"corpus: {lock['corpus_fingerprint']} -> "
        f"{candidate['corpus_fingerprint']}",
        f"projection format: {lock['projection_format_version']} -> "
        f"{candidate['projection_format_version']}",
    ]
    identity_lines = len(lines)
    pair = _build_pair(inputs, adapter)
    generation_path = inputs.root / _paths(adapter)[ProjectionMode.GENERATION]
    current_provenance = generation_path / "provenance.json"
    if current_provenance.is_file():
        try:
            loaded_entries = json.loads(
                current_provenance.read_text(encoding="utf-8")
            )["entries"]
            before_entries = loaded_entries if isinstance(loaded_entries, dict) else {}
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            before_entries = {}
    else:
        before_entries = {}
    after_entries = json.loads(pair[ProjectionMode.GENERATION][0].sidecar)["entries"]
    for entry_id in sorted(before_entries.keys() | after_entries.keys()):
        if entry_id not in before_entries:
            lines.append(f"added identity {entry_id}")
        elif entry_id not in after_entries:
            lines.append(f"removed identity {entry_id}")
        elif before_entries[entry_id] != after_entries[entry_id]:
            lines.append(f"changed identity {entry_id}")
    with tempfile.TemporaryDirectory(prefix="polc-diff-") as temp:
        staged = _stage_pair(pair, Path(temp), adapter)
        for mode, relative in _paths(adapter).items():
            before, after = _files(inputs.root / relative), _files(staged[mode])
            for name in sorted(before.keys() | after.keys()):
                change = (
                    "added"
                    if name not in before
                    else "removed"
                    if name not in after
                    else "changed"
                )
                if before.get(name) != after.get(name):
                    lines.append(f"{change} {relative}/{name}")
    identities_match = all(
        line.split(" -> ", 1)[0].split(": ", 1)[1]
        == line.split(" -> ", 1)[1]
        for line in lines[:identity_lines]
    )
    if len(lines) == identity_lines and identities_match:
        lines.append("no changes")
    return lines


def accept(inputs: Inputs, requested_adapter: str | None = None) -> list[str]:
    old = _read_lock(inputs.root, allow_projection_mismatch=True)
    old_adapter = old["adapter"]
    adapter = (
        old_adapter
        if requested_adapter is None
        else None
        if requested_adapter == "neutral"
        else requested_adapter
    )
    old_paths = _paths(old_adapter)
    paths = _paths(adapter)
    for mode, relative in old_paths.items():
        _assert_owned(inputs.root / relative, mode, old_adapter)
    for mode, relative in paths.items():
        destination = inputs.root / relative
        if relative not in old_paths.values():
            _assert_owned(destination, mode, adapter)
    candidate = _lock(inputs, adapter)
    with tempfile.TemporaryDirectory(prefix=".polc-accept-", dir=inputs.root) as temp:
        work = Path(temp)
        staged = _stage_pair(_build_pair(inputs, adapter), work / "outputs", adapter)
        lock_path = work / "lock.json"
        lock_path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
        replacements = [(staged[m], inputs.root / p) for m, p in paths.items()]
        replacements.extend(
            (None, inputs.root / relative)
            for relative in old_paths.values()
            if relative not in paths.values()
        )
        replacements.append((lock_path, inputs.root / ".polc/lock.json"))
        _install(replacements, work)
    return ["accepted executing release and rebuilt both outputs"]
