from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

KINDS = ("principle", "standard", "guideline", "pattern", "anti-pattern")
AXES = ("language_version", "compiler", "domain")
LANGUAGE_VERSIONS = ("14", "17", "20", "23")
COMPILERS = ("gcc", "clang")
ENFORCERS = ("compiler", "clang-format", "clang-tidy", "build", "review")


@dataclass(frozen=True)
class Destination:
    slug: str
    title: str
    read_when: str
    groups: tuple[str, ...] = ()
    before_topics: bool = False


DESTINATIONS = (
    Destination(
        "standard",
        "Coding standard",
        "writing any file — the mechanical rules a formatter or a compiler enforces",
        ("files-and-layout", "names", "layout-of-the-line", "comments"),
        before_topics=True,
    ),
    Destination(
        "exemplars",
        "Exemplars",
        "reaching for a whole compilable example of a recurring situation",
    ),
    Destination(
        "project-setup",
        "Project setup",
        "configuring the toolchain — language standard, warning set, formatter, "
        "test framework",
        ("toolchain",),
    ),
)
STANDARD_DOCUMENTS = tuple(d for d in DESTINATIONS if d.groups)
STANDARD_GROUPS = tuple(g for d in DESTINATIONS for g in d.groups)
RESERVED_SLUGS = (
    "index",
    "principles",
    "provenance",
    "skill",
    "configuration",
    "layers",
    "invariants",
) + tuple(
    d.slug for d in DESTINATIONS
)


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
    trigger: str | None = None


@dataclass(frozen=True)
class StandardEntry:
    id: str
    group: str
    enforced_by: str
    statement: str
    body: str
    attribution: tuple[Attribution, ...]
    path: Path
    applicability: dict[str, tuple[str, ...]] = field(default_factory=dict)


@dataclass(frozen=True)
class Exemplar:
    id: str
    statement: str
    situation: str
    body: str
    demonstrates: tuple[str, ...]
    directory: Path
    sources: tuple[Path, ...]
    applicability: dict[str, tuple[str, ...]] = field(default_factory=dict)


@dataclass(frozen=True)
class Topic:
    name: str
    slug: str
    read_when: str
    members: tuple[str, ...]
    cross_references: tuple[str, ...]


@dataclass(frozen=True)
class Configuration:
    name: str
    language_version: int
    compiler: str
    domain: str


@dataclass(frozen=True)
class TopicExclusion:
    topic: str
    reason: str


@dataclass(frozen=True)
class IdExclusion:
    id: str
    reason: str


@dataclass(frozen=True)
class IdReplacement:
    upstream: str
    local: str
    reason: str


@dataclass(frozen=True)
class ProjectConfiguration:
    configuration: Configuration
    exclude_topics: tuple[TopicExclusion, ...]
    exclude_ids: tuple[IdExclusion, ...]
    replace_ids: tuple[IdReplacement, ...]


@dataclass(frozen=True)
class MergeDecision:
    operation: str
    target: str
    reason: str
    local: str | None = None


@dataclass(frozen=True)
class CorpusLayers:
    policies: tuple[Policy, ...]
    topics: tuple[Topic, ...]
    standard: tuple[StandardEntry, ...]
    standard_topic_ids: tuple[str, ...]
    exemplars: tuple[Exemplar, ...]


@dataclass(frozen=True)
class EffectiveCorpus(CorpusLayers):
    decisions: tuple[MergeDecision, ...]


@dataclass(frozen=True)
class Exclusion:
    id: str
    axis: str


@dataclass(frozen=True)
class Identity:
    polc_version: str
    corpus_fingerprint: str
    configuration_source: str
    adapter: str | None
    overlay_fingerprint: str | None = None
    decisions: tuple[MergeDecision, ...] = ()
