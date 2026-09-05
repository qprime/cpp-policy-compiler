from __future__ import annotations

import hashlib
import json
import tempfile
import zipfile
from importlib.metadata import version
from pathlib import Path, PurePosixPath

from .corpus import fingerprint
from .model import PolcError, ProjectionMode
from .render import write
from .resources import PROJECTION_FORMAT_VERSION, CorpusPaths, installed_corpus

ARCHIVE_SCHEMA_VERSION = 1
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _archive_name(configuration: Path) -> str:
    return f"{configuration.stem}-polc-{version('polc')}.zip"


def _zip_entry(name: str, data: bytes) -> tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(name, ARCHIVE_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    info.create_system = 3
    return info, data


def build_archive(
    configuration: Path, destination: Path, corpus: CorpusPaths | None = None
) -> Path:
    from .cli import _build_projection

    corpus = corpus or installed_corpus()
    files: dict[str, bytes] = {}
    config_name = ""
    with tempfile.TemporaryDirectory(prefix="polc-release-") as temporary:
        stage = Path(temporary)
        for mode in ProjectionMode:
            projection, _, config, exemplars = _build_projection(
                configuration,
                corpus.policies,
                corpus.standard,
                corpus.exemplars,
                None,
                mode,
            )
            config_name = config.name
            output = stage / mode.value
            write(projection, exemplars, output)
            for path in sorted(output.rglob("*")):
                if path.is_file():
                    files[path.relative_to(stage).as_posix()] = path.read_bytes()
    corpus_fingerprint = fingerprint(
        corpus.policies, corpus.standard, corpus.exemplars
    )
    manifest = {
        "schema_version": ARCHIVE_SCHEMA_VERSION,
        "polc_version": version("polc"),
        "projection_format_version": PROJECTION_FORMAT_VERSION,
        "corpus_fingerprint": corpus_fingerprint,
        "configuration": config_name,
        "files": {name: _digest(data) for name, data in sorted(files.items())},
    }
    files["manifest.json"] = (
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    ).encode()
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / _archive_name(configuration)
    with zipfile.ZipFile(archive, "w") as output:
        for name, data in sorted(files.items()):
            info, payload = _zip_entry(name, data)
            output.writestr(info, payload)
    verify_archive(archive, corpus_fingerprint)
    return archive


def build_stock_archives(destination: Path) -> list[Path]:
    corpus = installed_corpus()
    configurations = sorted(
        path
        for path in corpus.configurations.glob("*.md")
        if path.name != "README.md"
    )
    if not configurations:
        raise PolcError([f"{corpus.configurations}: no stock configurations found"])
    return [build_archive(path, destination, corpus) for path in configurations]


def verify_archive(archive: Path, expected_fingerprint: str | None = None) -> None:
    try:
        with zipfile.ZipFile(archive) as source:
            names = source.namelist()
            if any(
                PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts
                for name in names
            ):
                raise PolcError([f"{archive}: archive contains an unsafe path"])
            if len(names) != len(set(names)) or "manifest.json" not in names:
                raise PolcError([f"{archive}: invalid archive member list"])
            manifest = json.loads(source.read("manifest.json"))
            expected_keys = {
                "schema_version",
                "polc_version",
                "projection_format_version",
                "corpus_fingerprint",
                "configuration",
                "files",
            }
            if not isinstance(manifest, dict) or set(manifest) != expected_keys:
                raise PolcError([f"{archive}: invalid manifest structure"])
            if manifest["schema_version"] != ARCHIVE_SCHEMA_VERSION:
                raise PolcError([f"{archive}: unsupported archive schema"])
            if manifest["polc_version"] != version("polc"):
                raise PolcError([f"{archive}: package version mismatch"])
            if manifest["projection_format_version"] != PROJECTION_FORMAT_VERSION:
                raise PolcError([f"{archive}: projection format mismatch"])
            if (
                expected_fingerprint is not None
                and manifest["corpus_fingerprint"] != expected_fingerprint
            ):
                raise PolcError([f"{archive}: corpus fingerprint mismatch"])
            recorded = manifest["files"]
            actual_names = set(names) - {"manifest.json"}
            if not isinstance(recorded, dict) or set(recorded) != actual_names:
                raise PolcError([f"{archive}: manifest file list mismatch"])
            for name, digest in recorded.items():
                if _digest(source.read(name)) != digest:
                    raise PolcError([f"{archive}: digest mismatch for {name}"])
            for mode in ProjectionMode:
                provenance = json.loads(source.read(f"{mode.value}/provenance.json"))
                identity = provenance["projection"]
                if identity.get("mode") != mode.value:
                    raise PolcError([f"{archive}: {mode.value} mode mismatch"])
                if identity.get("corpus_fingerprint") != manifest["corpus_fingerprint"]:
                    raise PolcError([f"{archive}: projection corpus mismatch"])
                if identity.get("projection_format_version") != PROJECTION_FORMAT_VERSION:
                    raise PolcError([f"{archive}: projection format mismatch"])
    except (
        OSError,
        zipfile.BadZipFile,
        json.JSONDecodeError,
        KeyError,
        TypeError,
    ) as exc:
        raise PolcError([f"{archive}: cannot verify archive: {exc}"]) from exc
