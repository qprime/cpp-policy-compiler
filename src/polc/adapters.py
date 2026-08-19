from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, replace

from .model import Configuration, PolcError
from .render import Projection

NEUTRAL_ENTRY = "index.md"
DESCRIPTION_LIMIT = 1024


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower())[:64].strip("-")


def _quote(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def _description(config: Configuration, map_titles: tuple[str, ...]) -> str:
    covers = ", ".join(title.lower() for title in map_titles)
    text = (
        f"C++ engineering policy for {config.name} — C++{config.language_version}, "
        f"{config.compiler}, {config.domain}. Read before writing or changing any "
        f"C++ in this project. Covers: {covers}."
    )
    if len(text) > DESCRIPTION_LIMIT:
        raise PolcError(
            [
                f"skill description is {len(text)} characters, over the "
                f"{DESCRIPTION_LIMIT}-character limit"
            ]
        )
    return text


def _skill_frontmatter(config: Configuration, map_titles: tuple[str, ...]) -> str:
    name = _slugify(config.name)
    if not name:
        raise PolcError(
            [
                f"configuration name '{config.name}' slugifies to nothing; "
                "a skill needs a name of at least one alphanumeric character"
            ]
        )
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {_quote(_description(config, map_titles))}\n"
        "---\n\n"
    )


@dataclass(frozen=True)
class Adapter:
    entry: str
    frontmatter: Callable[[Configuration, tuple[str, ...]], str]


ADAPTERS_BY_NAME = {"claude-code": Adapter("SKILL.md", _skill_frontmatter)}
ADAPTERS = tuple(ADAPTERS_BY_NAME)


def _lookup(adapter: str) -> Adapter:
    try:
        return ADAPTERS_BY_NAME[adapter]
    except KeyError:
        raise PolcError(
            [f"unknown adapter '{adapter}': known adapters are {', '.join(ADAPTERS)}"]
        ) from None


def entry_name(adapter: str | None) -> str:
    return NEUTRAL_ENTRY if adapter is None else _lookup(adapter).entry


def apply(
    adapter: str | None, projection: Projection, config: Configuration
) -> Projection:
    if adapter is None:
        return projection
    frontmatter = _lookup(adapter).frontmatter(config, projection.map_titles)
    return replace(projection, entry=frontmatter + projection.entry)
