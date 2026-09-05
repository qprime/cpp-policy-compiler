from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path

from .model import Configuration, PolcError, ProjectionMode
from .render import Projection

NEUTRAL_ENTRY = "index.md"
DESCRIPTION_LIMIT = 1024

NEUTRAL_WIRING = (
    "Add to this project's instruction file (CLAUDE.md, AGENTS.md, or equivalent):\n"
    "\n"
    "    Read `{path}` before writing or changing any C++ in this\n"
    "    project. It maps each situation to the one document that governs it."
)
NEUTRAL_REVIEW_WIRING = (
    "Add to this project's review instructions:\n"
    "\n"
    "    Read `{path}` before reviewing any C++ change in this project. It maps\n"
    "    observable evidence to the documents that govern the review."
)

ABSOLUTE_PATH_NOTE = (
    "Replace that absolute path with one relative to the target repository root."
)


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower())[:64].strip("-")


def _quote(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def _description(
    config: Configuration, map_titles: tuple[str, ...], mode: ProjectionMode
) -> str:
    covers = ", ".join(title.lower() for title in map_titles)
    purpose = (
        "Use when reviewing existing C++ changes"
        if mode == ProjectionMode.REVIEW
        else "Read before writing or changing any C++ in this project"
    )
    text = (
        f"C++ engineering policy for {config.name} — C++{config.language_version}, "
        f"{config.compiler}, {config.domain}. {purpose}. Covers: {covers}."
    )
    if len(text) > DESCRIPTION_LIMIT:
        raise PolcError(
            [
                f"skill description is {len(text)} characters, over the "
                f"{DESCRIPTION_LIMIT}-character limit"
            ]
        )
    return text


def _skill_frontmatter(
    config: Configuration, map_titles: tuple[str, ...], mode: ProjectionMode
) -> str:
    name = _slugify(f"{config.name}-{mode.value}")
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
        f"description: {_quote(_description(config, map_titles, mode))}\n"
        "---\n\n"
    )


@dataclass(frozen=True)
class Adapter:
    entry: str
    frontmatter: Callable[[Configuration, tuple[str, ...], ProjectionMode], str]
    wiring: str | None


ADAPTERS_BY_NAME = {"claude-code": Adapter("SKILL.md", _skill_frontmatter, None)}
ADAPTERS = tuple(ADAPTERS_BY_NAME)


def destinations(adapter: str | None) -> dict[ProjectionMode, Path]:
    if adapter is None:
        return {
            ProjectionMode.GENERATION: Path("policy/generation"),
            ProjectionMode.REVIEW: Path("policy/review"),
        }
    _lookup(adapter)
    return {
        ProjectionMode.GENERATION: Path(".claude/skills/cpp-policy-generation"),
        ProjectionMode.REVIEW: Path(".claude/skills/cpp-policy-review"),
    }


def _lookup(adapter: str) -> Adapter:
    try:
        return ADAPTERS_BY_NAME[adapter]
    except KeyError:
        raise PolcError(
            [f"unknown adapter '{adapter}': known adapters are {', '.join(ADAPTERS)}"]
        ) from None


def entry_name(adapter: str | None) -> str:
    return NEUTRAL_ENTRY if adapter is None else _lookup(adapter).entry


def wiring_note(
    adapter: str | None,
    out_dir: Path,
    projection: Projection,
) -> str | None:
    if adapter is None:
        wiring = (
            NEUTRAL_REVIEW_WIRING
            if projection.mode == ProjectionMode.REVIEW
            else NEUTRAL_WIRING
        )
    else:
        wiring = _lookup(adapter).wiring
    if wiring is None:
        return None
    note = wiring.format(path=out_dir / projection.entry_name)
    if out_dir.is_absolute():
        note = f"{note}\n\n{ABSOLUTE_PATH_NOTE}"
    return note


def apply(
    adapter: str | None, projection: Projection, config: Configuration
) -> Projection:
    if adapter is None:
        return projection
    frontmatter = _lookup(adapter).frontmatter(
        config, projection.map_titles, projection.mode
    )
    return replace(projection, entry=frontmatter + projection.entry)
