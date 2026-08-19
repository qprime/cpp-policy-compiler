from __future__ import annotations

from pathlib import Path

from .frontmatter import (
    parse_applicability,
    parse_frontmatter,
    required_str,
    split_statement,
    string_list,
)
from .model import Exemplar, PolcError

EXEMPLAR_KEYS = {
    "id",
    "demonstrates",
    "applicability",
}


def _origin(path: Path) -> str:
    return f"{path.parent.name}/{path.name}"


def _parse_exemplar(path: Path) -> Exemplar:
    origin = _origin(path)
    frontmatter, markdown = parse_frontmatter(path.read_text(encoding="utf-8"), origin)
    errors: list[str] = []

    unknown = sorted(frontmatter.keys() - EXEMPLAR_KEYS)
    if unknown:
        errors.append(f"{origin}: unknown frontmatter keys: {', '.join(unknown)}")

    exemplar_id = required_str(frontmatter.get("id"), origin, "id", errors)
    demonstrates = string_list(
        frontmatter.get("demonstrates"), origin, "demonstrates", errors
    )
    applicability = parse_applicability(
        frontmatter.get("applicability"), origin, errors
    )
    try:
        statement, body = split_statement(markdown, origin)
    except PolcError as exc:
        errors.extend(exc.errors)
        statement, body = "", ""

    if errors:
        raise PolcError(errors)
    directory = path.parent
    sources = tuple(
        sorted(
            item.relative_to(directory)
            for item in directory.rglob("*")
            if item.is_file() and item != path
        )
    )
    return Exemplar(
        id=exemplar_id,
        statement=statement,
        body=body,
        demonstrates=demonstrates,
        directory=directory,
        sources=sources,
        applicability=applicability,
    )


def load_exemplars(exemplars_dir: Path) -> list[Exemplar]:
    errors: list[str] = []
    exemplars: list[Exemplar] = []
    directories = sorted(d for d in exemplars_dir.glob("EXM-*") if d.is_dir())
    if not directories:
        raise PolcError([f"{exemplars_dir}: no exemplar directories found"])
    for directory in directories:
        path = directory / "exemplar.md"
        if not path.is_file():
            errors.append(f"{directory.name}: directory holds no exemplar.md")
            continue
        try:
            exemplars.append(_parse_exemplar(path))
        except PolcError as exc:
            errors.extend(exc.errors)
    if errors:
        raise PolcError(errors)
    return exemplars
