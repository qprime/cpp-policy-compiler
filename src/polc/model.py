from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

KINDS = ("principle", "standard", "guideline", "pattern", "anti-pattern")
AXES = ("language_version", "compiler", "domain")
LANGUAGE_VERSIONS = ("14", "17", "20", "23")
COMPILERS = ("gcc", "clang")


class PolcError(Exception):
    def __init__(self, errors: list[str]):
        super().__init__("\n".join(errors))
        self.errors = list(errors)


@dataclass(frozen=True)
class Attribution:
    source: str
    locator: str
    upstream: tuple[str, ...] = ()


@dataclass(frozen=True)
class Policy:
    id: str
    kind: str
    statement: str
    body: str
    attribution: tuple[Attribution, ...]
    path: Path
    precedence: int | None = None
    applicability: dict[str, tuple[str, ...]] = field(default_factory=dict)
    replacement: tuple[str, ...] = ()
    enforcement: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Topic:
    name: str
    slug: str
    read_when: str
    members: tuple[str, ...]
    cross_references: tuple[str, ...]


@dataclass(frozen=True)
class Budgets:
    entry_chars: int
    topic_chars: int


@dataclass(frozen=True)
class Configuration:
    name: str
    language_version: int
    compiler: str
    domain: str
    budgets: Budgets


@dataclass(frozen=True)
class Exclusion:
    policy_id: str
    axis: str
