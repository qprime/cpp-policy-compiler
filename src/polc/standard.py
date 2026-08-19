from __future__ import annotations

from pathlib import Path

from .frontmatter import (
    parse_applicability,
    parse_attribution,
    parse_frontmatter,
    required_str,
    split_statement,
)
from .model import PolcError, StandardEntry

STANDARD_KEYS = {
    "id",
    "group",
    "enforced_by",
    "applicability",
    "attribution",
}


def _parse_entry(path: Path) -> StandardEntry:
    frontmatter, markdown = parse_frontmatter(
        path.read_text(encoding="utf-8"), path.name
    )
    errors: list[str] = []

    unknown = sorted(frontmatter.keys() - STANDARD_KEYS)
    if unknown:
        errors.append(f"{path.name}: unknown frontmatter keys: {', '.join(unknown)}")

    entry_id = required_str(frontmatter.get("id"), path.name, "id", errors)
    group = required_str(frontmatter.get("group"), path.name, "group", errors)
    enforced_by = required_str(
        frontmatter.get("enforced_by"), path.name, "enforced_by", errors
    )

    attribution = parse_attribution(frontmatter.get("attribution"), path.name, errors)
    applicability = parse_applicability(
        frontmatter.get("applicability"), path.name, errors
    )
    try:
        statement, body = split_statement(markdown, path.name)
    except PolcError as exc:
        errors.extend(exc.errors)
        statement, body = "", ""

    if errors:
        raise PolcError(errors)
    return StandardEntry(
        id=entry_id,
        group=group,
        enforced_by=enforced_by,
        statement=statement,
        body=body,
        attribution=attribution,
        path=path,
        applicability=applicability,
    )


def load_standard(standard_dir: Path) -> list[StandardEntry]:
    errors: list[str] = []
    entries: list[StandardEntry] = []
    paths = sorted(standard_dir.glob("STD-*.md"))
    if not paths:
        raise PolcError([f"{standard_dir}: no standard entry files found"])
    for path in paths:
        try:
            entries.append(_parse_entry(path))
        except PolcError as exc:
            errors.extend(exc.errors)
    if errors:
        raise PolcError(errors)
    return entries
