from __future__ import annotations

import yaml

from .model import Attribution, PolcError

ATTRIBUTION_KEYS = {"source", "locator", "upstream"}


def parse_frontmatter(text: str, origin: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise PolcError([f"{origin}: file does not start with a frontmatter block"])
    end = text.find("\n---\n", 4)
    if end == -1:
        raise PolcError([f"{origin}: frontmatter block is not closed"])
    try:
        frontmatter = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        raise PolcError([f"{origin}: frontmatter is not valid YAML: {exc}"]) from exc
    if not isinstance(frontmatter, dict):
        raise PolcError([f"{origin}: frontmatter is not a mapping"])
    return frontmatter, text[end + 5 :]


def split_statement(markdown: str, origin: str) -> tuple[str, str]:
    lines = markdown.split("\n")
    fenced = False
    h1_indexes = []
    for index, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("# "):
            h1_indexes.append(index)
    if len(h1_indexes) != 1:
        raise PolcError(
            [f"{origin}: expected exactly one H1, found {len(h1_indexes)}"]
        )
    at = h1_indexes[0]
    statement = lines[at][2:].strip()
    body = "\n".join(lines[at + 1 :]).strip("\n")
    return statement, body


def required_str(value: object, origin: str, key: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value:
        errors.append(f"{origin}: '{key}' must be a non-empty string")
        return ""
    return value


def string_list(value: object, origin: str, key: str, errors: list[str]) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        errors.append(f"{origin}: '{key}' must be a list of strings")
        return ()
    return tuple(value)


def parse_attribution(value: object, origin: str, errors: list[str]) -> tuple[Attribution, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        errors.append(f"{origin}: 'attribution' must be a list")
        return ()
    entries = []
    for entry in value:
        if not isinstance(entry, dict) or not ATTRIBUTION_KEYS >= entry.keys():
            errors.append(f"{origin}: attribution entries carry source, locator, and optional upstream")
            continue
        source = entry.get("source")
        locator = entry.get("locator")
        if not isinstance(source, str) or not isinstance(locator, str):
            errors.append(f"{origin}: attribution source and locator must be strings")
            continue
        upstream = entry.get("upstream", [])
        if not isinstance(upstream, list) or not all(isinstance(u, str) for u in upstream):
            errors.append(f"{origin}: attribution upstream must be a list of strings")
            continue
        entries.append(Attribution(source, locator, tuple(upstream)))
    return tuple(entries)


def parse_applicability(value: object, origin: str, errors: list[str]) -> dict[str, tuple[str, ...]]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        errors.append(f"{origin}: 'applicability' must be a mapping of axis to value list")
        return {}
    marks = {}
    for axis, values in value.items():
        if not isinstance(axis, str) or not isinstance(values, list) or not values:
            errors.append(f"{origin}: applicability axis '{axis}' must map to a non-empty list")
            continue
        marks[axis] = tuple(str(v) for v in values)
    return marks
