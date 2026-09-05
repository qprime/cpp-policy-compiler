from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

PROJECTION_FORMAT_VERSION = 1
LOCK_SCHEMA_VERSION = 2
PROJECT_LAYOUT_VERSION = 1


@dataclass(frozen=True)
class CorpusPaths:
    policies: Path
    standard: Path
    exemplars: Path
    configurations: Path


def installed_corpus() -> CorpusPaths:
    root = Path(str(files("polc").joinpath("data")))
    paths = CorpusPaths(
        root / "policies",
        root / "standard",
        root / "exemplars",
        root / "configurations",
    )
    missing = [str(path) for path in paths.__dict__.values() if not path.is_dir()]
    if missing:
        from .model import PolcError

        raise PolcError(
            ["installed polc distribution is missing corpus roots: " + ", ".join(missing)]
        )
    return paths
