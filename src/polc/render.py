from __future__ import annotations

import json
import shutil
import textwrap
from dataclasses import dataclass
from pathlib import Path

from .links import CORPUS_TARGET, scan_links
from .model import (
    DESTINATIONS,
    STANDARD_DOCUMENTS,
    Configuration,
    Destination,
    Exclusion,
    Exemplar,
    Identity,
    PolcError,
    Policy,
    StandardEntry,
    Topic,
)

MARKS = {
    "standard": "MUST",
    "guideline": "SHOULD",
    "pattern": "THIS WAY",
    "anti-pattern": "NEVER",
}

LEGEND = (
    "## Marks",
    "",
    "| Mark | Meaning |",
    "|---|---|",
    "| MUST | A standard. Follow it. |",
    "| SHOULD | A guideline. Follow it unless the situation says otherwise, "
    "and say why. |",
    "| THIS WAY | A pattern. The shape to reach for. |",
    "| NEVER | An anti-pattern. The replacement is named beneath it. |",
)

MAP_ROUTING = (
    "Read the document whose line matches what you are about to do. Read the coding\n"
    "standard for any file; read one topic for the decision in front of you."
)

PRINCIPLES = "principles"
PRINCIPLES_DOCUMENT = f"{PRINCIPLES}.md"
PRINCIPLES_TITLE = "Principles"

LAYERS_DOCUMENT = "layers.md"
LAYERS_TITLE = "Layers"
INVARIANTS_DOCUMENT = "invariants.md"
INVARIANTS_TITLE = "Invariants"

SEED_NOTICE = (
    "polc seeds this document once and never overwrites it. Every other document\n"
    "in this directory is rewritten on every build; this one is the project's to\n"
    "write and to keep."
)

SEEDS = {
    LAYERS_DOCUMENT: (
        f"# {LAYERS_TITLE}\n"
        "\n"
        f"{SEED_NOTICE}\n"
        "\n"
        "Write the layers of this project here: what each one is, what it may depend\n"
        "on, and how code in it reports failure. The procedure in the entry document\n"
        "sends the reader here before they choose how a function signals failure.\n"
    ),
    INVARIANTS_DOCUMENT: (
        f"# {INVARIANTS_TITLE}\n"
        "\n"
        f"{SEED_NOTICE}\n"
        "\n"
        "Write the load-bearing properties of this project's subsystems here: what\n"
        "must hold, where it is enforced, and what breaks when it stops holding. The\n"
        "procedure in the entry document sends the reader here before they touch a\n"
        "subsystem.\n"
    ),
}
SEED_DOCUMENTS = tuple(SEEDS)

TRIGGER_COLUMN = "When you are about to"

EXEMPLARS = next(d for d in DESTINATIONS if d.slug == "exemplars")
EXEMPLARS_PREAMBLE = (
    "Whole compilable source for a recurring situation. Each tree sits under\n"
    "`exemplars/` and is laid out from the project root, so a copy into a real "
    "project\nneeds no edits."
)


@dataclass(frozen=True)
class Projection:
    entry: str
    entry_name: str
    map_titles: tuple[str, ...]
    principles: str | None
    topic_documents: dict[str, str]
    standard_documents: dict[str, str]
    exemplars: str | None
    sidecar: str
    identity: Identity
    omitted_topics: tuple[str, ...]
    omitted_standard_documents: tuple[str, ...]
    dropped_references: tuple[str, ...]
    trigger_coverage: tuple[int, int]

    def documents(self) -> dict[str, str]:
        documents = {self.entry_name: self.entry}
        if self.principles is not None:
            documents[PRINCIPLES_DOCUMENT] = self.principles
        for slug, text in self.topic_documents.items():
            documents[f"{slug}.md"] = text
        for slug, text in self.standard_documents.items():
            documents[f"{slug}.md"] = text
        if self.exemplars is not None:
            documents["exemplars.md"] = self.exemplars
        documents.update(SEEDS)
        documents["configuration.md"] = self.identity.configuration_source
        return documents


def _compact_ref(item: Policy | StandardEntry) -> str:
    upstream: list[str] = []
    for attribution in item.attribution:
        for citation in attribution.upstream:
            if citation not in upstream:
                upstream.append(citation)
    if upstream:
        return f"{item.id} · {', '.join(upstream)}"
    return item.id


def _order_topic(topic: Topic, included_by_id: dict[str, Policy]) -> list[Policy]:
    ordered = [included_by_id[m] for m in topic.members if m in included_by_id]
    member_set = set(topic.members)
    moved: set[str] = set()
    for member in topic.members:
        policy = included_by_id.get(member)
        if policy is None or policy.kind != "anti-pattern":
            continue
        anchors = [
            target
            for target in policy.replacement
            if target in member_set and target in included_by_id
        ]
        if not anchors:
            continue
        ordered.remove(policy)
        ids = [p.id for p in ordered]
        index = max(ids.index(target) for target in anchors)
        while index + 1 < len(ordered) and ordered[index + 1].id in moved:
            index += 1
        ordered.insert(index + 1, policy)
        moved.add(policy.id)
    return ordered


def _entry_block(
    heading: str, reference: str, body: str, demonstrated_by: list[str] | None = None
) -> list[str]:
    lines = [heading, "", reference, "", body, ""]
    if demonstrated_by:
        links = ", ".join(f"[{exm}](exemplars.md)" for exm in demonstrated_by)
        lines.extend([f"Demonstrated by: {links}", ""])
    return lines


def _resolve_body_links(
    body: str, origin: str, home_document: dict[str, str], dropped: list[str]
) -> str:
    edits: list[tuple[int, int, str]] = []
    for link in scan_links(body):
        match = CORPUS_TARGET.fullmatch(link.path)
        if match is None:
            continue
        target = match.group(1)
        destination = home_document.get(target)
        if destination is None:
            edits.append((link.start, link.end, link.text))
            dropped.append(
                f"{origin}: link to {target} not emitted by this configuration; "
                "kept as text"
            )
        else:
            edits.append((link.start, link.end, f"[{link.text}]({destination})"))
    for start, end, replacement in reversed(edits):
        body = body[:start] + replacement + body[end:]
    return body


def _banner(config: Configuration) -> str:
    return (
        f"<!-- Generated by polc from configuration {config.name}. "
        "Edits are overwritten. -->\n\n"
    )


def _render_principles_document(
    config: Configuration,
    principles: list[Policy],
    home_document: dict[str, str],
    dropped: list[str],
) -> str:
    lines = [
        f"{config.name} › {PRINCIPLES_TITLE}",
        "",
        "Read when: always. These govern every decision in this project.",
        "",
    ]
    for principle in principles:
        lines.extend(
            _entry_block(
                f"## {principle.statement}",
                _compact_ref(principle),
                _resolve_body_links(
                    principle.body, principle.path.name, home_document, dropped
                ),
            )
        )
    lines.extend(LEGEND)
    return "\n".join(lines).rstrip("\n") + "\n"


def _procedure(has_principles: bool, has_exemplars: bool) -> list[str]:
    steps: list[str] = []
    if has_exemplars:
        steps.append(
            "Take the shape from the nearest exemplar. "
            f"[{EXEMPLARS.title}]({EXEMPLARS.slug}.md) indexes them by situation."
        )
    triggers = (
        "Check each construct you write against the trigger table at the head of "
        "the document the map names below."
    )
    if has_principles:
        triggers += (
            f" [{PRINCIPLES_TITLE}]({PRINCIPLES_DOCUMENT}) governs what no trigger "
            "row matches."
        )
    steps.append(triggers)
    steps.append(
        f"Read [{LAYERS_TITLE}]({LAYERS_DOCUMENT}) for how code at this layer "
        "reports failure."
    )
    steps.append(
        f"Read [{INVARIANTS_TITLE}]({INVARIANTS_DOCUMENT}) before you touch a "
        "subsystem."
    )
    lines = ["## Procedure", "", "Take these in order for every change.", ""]
    for number, step in enumerate(steps, start=1):
        lines.append(
            textwrap.fill(
                f"{number}. {step}", width=79, subsequent_indent="   "
            )
        )
    lines.append("")
    return lines


def _trigger_table(ordered: list[Policy]) -> list[str]:
    rows = [
        f"| {policy.trigger} | {MARKS[policy.kind]} | {policy.id} |"
        for policy in ordered
        if policy.trigger
    ]
    if not rows:
        return []
    return [f"| {TRIGGER_COLUMN} | | Rule |", "|---|---|---|", *rows, ""]


def _situation_index(admitted: list[Exemplar]) -> list[str]:
    rows = [
        f"| {exemplar.situation} | {exemplar.id} |" for exemplar in admitted
    ]
    return [f"| {TRIGGER_COLUMN} | Exemplar |", "|---|---|", *rows, ""]


def _render_entry_document(
    config: Configuration,
    identity: Identity,
    has_principles: bool,
    has_exemplars: bool,
    emitted: list[tuple[Topic, list[Policy]]],
    written: set[str],
) -> tuple[str, tuple[str, ...]]:
    lines = [
        f"# {config.name}",
        "",
        f"- Standard: C++{config.language_version}",
        f"- Compiler: {config.compiler}",
        f"- Domain: {config.domain}",
        f"- Generated by polc {identity.polc_version} from corpus "
        f"{identity.corpus_fingerprint}",
        "",
        "Per-standard tables in these documents read against the declared standard above.",
        "",
    ]
    lines.extend(_procedure(has_principles, has_exemplars))
    lines.extend(["## Map", "", MAP_ROUTING, ""])

    titles: list[str] = []

    def destination_line(destination: Destination) -> None:
        if destination.slug not in written:
            return
        titles.append(destination.title)
        lines.append(
            f"- [{destination.title}]({destination.slug}.md) — {destination.read_when}"
        )

    for destination in DESTINATIONS:
        if destination.before_topics:
            destination_line(destination)
    for topic, _ in emitted:
        titles.append(topic.name)
        lines.append(f"- [{topic.name}]({topic.slug}.md) — {topic.read_when}")
    for destination in DESTINATIONS:
        if not destination.before_topics:
            destination_line(destination)
    return "\n".join(lines).rstrip("\n") + "\n", tuple(titles)


def _render_topic_document(
    config: Configuration,
    topic: Topic,
    ordered: list[Policy],
    included_by_id: dict[str, Policy],
    home_topic: dict[str, Topic],
    demonstrated_by: dict[str, list[str]],
    home_document: dict[str, str],
    dropped: list[str],
) -> str:
    lines = [
        f"{config.name} › {topic.name}",
        "",
        f"Read when: {topic.read_when}",
        "",
    ]
    lines.extend(_trigger_table(ordered))
    for policy in ordered:
        lines.extend(
            _entry_block(
                f"## {MARKS[policy.kind]} — {policy.statement}",
                _compact_ref(policy),
                _resolve_body_links(
                    policy.body, policy.path.name, home_document, dropped
                ),
                demonstrated_by.get(policy.id),
            )
        )
    see_also = []
    for target in topic.cross_references:
        policy = included_by_id.get(target)
        if policy is None:
            dropped.append(
                f"{topic.name}: cross-reference {target} dropped (excluded by applicability)"
            )
            continue
        see_also.append(
            f"[{policy.id} — {policy.statement}]({home_topic[target].slug}.md)"
        )
    if see_also:
        lines.append(f"See also: {', '.join(see_also)}")
    return "\n".join(lines).rstrip("\n") + "\n"


def _group_heading(group: str) -> str:
    return group.replace("-", " ").capitalize()


def _standard_ref(entry: StandardEntry) -> str:
    return f"{_compact_ref(entry)} · enforced by {entry.enforced_by}"


def _render_standard_document(
    config: Configuration,
    title: str,
    groups: tuple[str, ...],
    members: list[StandardEntry],
    demonstrated_by: dict[str, list[str]],
    home_document: dict[str, str],
    dropped: list[str],
) -> str:
    lines = [f"{config.name} › {title}", ""]
    for group in groups:
        grouped = sorted((e for e in members if e.group == group), key=lambda e: e.id)
        if not grouped:
            continue
        lines.extend([f"## {_group_heading(group)}", ""])
        for entry in grouped:
            lines.extend(
                _entry_block(
                    f"### {entry.statement}",
                    _standard_ref(entry),
                    _resolve_body_links(
                        entry.body, entry.path.name, home_document, dropped
                    ),
                    demonstrated_by.get(entry.id),
                )
            )
    return "\n".join(lines).rstrip("\n") + "\n"


def _render_exemplars_document(
    config: Configuration,
    admitted: list[Exemplar],
    citations: dict[str, list[str]],
    home_document: dict[str, str],
    dropped: list[str],
) -> str:
    lines = [
        f"{config.name} › {EXEMPLARS.title}",
        "",
        EXEMPLARS_PREAMBLE,
        "",
    ]
    lines.extend(_situation_index(admitted))
    for exemplar in admitted:
        directory = f"exemplars/{exemplar.directory.name}/"
        lines.extend(
            [
                f"## {exemplar.statement}",
                "",
                f"{exemplar.id} · [{directory}]({directory})",
                "",
                _resolve_body_links(
                    exemplar.body,
                    f"{exemplar.directory.name}/exemplar.md",
                    home_document,
                    dropped,
                ),
                "",
            ]
        )
        rendered = citations[exemplar.id]
        if rendered:
            links = ", ".join(
                f"[{target}]({home_document[target]})" for target in rendered
            )
            lines.extend([f"Demonstrates: {links}", ""])
    return "\n".join(lines).rstrip("\n") + "\n"


def _attribution_records(item: Policy | StandardEntry) -> list[dict[str, object]]:
    return [
        {"source": a.source, "locator": a.locator, "upstream": list(a.upstream)}
        for a in item.attribution
    ]


def _render_sidecar(
    config: Configuration,
    identity: Identity,
    principles: list[Policy],
    emitted: list[tuple[Topic, list[Policy]]],
    standard: list[tuple[Destination, list[StandardEntry]]],
    admitted: list[Exemplar],
    citations: dict[str, list[str]],
) -> str:
    entries: dict[str, dict[str, object]] = {}

    def record(policy: Policy, topic: str) -> None:
        entries[policy.id] = {
            "layer": "policy",
            "kind": policy.kind,
            "topic": topic,
            "statement": policy.statement,
            "attribution": _attribution_records(policy),
            "file": policy.path.name,
        }

    for principle in principles:
        record(principle, PRINCIPLES)
    for topic, ordered in emitted:
        for policy in ordered:
            record(policy, topic.slug)
    for destination, members in standard:
        for entry in members:
            entries[entry.id] = {
                "layer": "standard",
                "group": entry.group,
                "enforced_by": entry.enforced_by,
                "document": f"{destination.slug}.md",
                "statement": entry.statement,
                "attribution": _attribution_records(entry),
                "file": entry.path.name,
            }
    for exemplar in admitted:
        entries[exemplar.id] = {
            "layer": "exemplar",
            "statement": exemplar.statement,
            "directory": f"exemplars/{exemplar.directory.name}",
            "demonstrates": citations[exemplar.id],
            "file": "exemplar.md",
        }
    data = {
        "projection": {
            "polc_version": identity.polc_version,
            "corpus_fingerprint": identity.corpus_fingerprint,
            "configuration": config.name,
            "adapter": identity.adapter,
        },
        "entries": {entry_id: entries[entry_id] for entry_id in sorted(entries)},
    }
    if identity.overlay_fingerprint is not None:
        data["projection"]["overlay_fingerprint"] = identity.overlay_fingerprint
        data["projection"]["merge_decisions"] = [
            {
                "operation": decision.operation,
                "target": decision.target,
                "reason": decision.reason,
                **({"local": decision.local} if decision.local is not None else {}),
            }
            for decision in identity.decisions
        ]
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def _resolve_citations(
    admitted: list[Exemplar],
    included_by_id: dict[str, Policy],
    included_standard_ids: set[str],
    exclusions: list[Exclusion],
    dropped: list[str],
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    axis_by_id = {exclusion.id: exclusion.axis for exclusion in exclusions}
    citations: dict[str, list[str]] = {}
    demonstrated_by: dict[str, list[str]] = {}
    for exemplar in admitted:
        rendered: list[str] = []
        for target in exemplar.demonstrates:
            if target in included_by_id or target in included_standard_ids:
                rendered.append(target)
            else:
                dropped.append(
                    f"{exemplar.id}: citation {target} "
                    f"(excluded by {axis_by_id[target]})"
                )
        citations[exemplar.id] = rendered
        if not rendered:
            dropped.append(
                f"{exemplar.id}: every citation dropped; the section renders "
                "without a citation list"
            )
        for target in rendered:
            policy = included_by_id.get(target)
            if policy is not None and policy.kind == "principle":
                continue
            demonstrated_by.setdefault(target, []).append(exemplar.id)
    return citations, demonstrated_by


def render(
    topics: list[Topic],
    config: Configuration,
    included: list[Policy],
    included_standard: list[StandardEntry],
    admitted_exemplars: list[Exemplar],
    exclusions: list[Exclusion],
    entry_name: str,
    identity: Identity,
) -> Projection:
    included_by_id = {p.id: p for p in included}
    home_topic = {member: topic for topic in topics for member in topic.members}

    principles = sorted(
        (p for p in included if p.kind == "principle"),
        key=lambda p: p.precedence or 0,
    )
    emitted: list[tuple[Topic, list[Policy]]] = []
    omitted: list[str] = []
    for topic in topics:
        ordered = _order_topic(topic, included_by_id)
        if ordered:
            emitted.append((topic, ordered))
        else:
            omitted.append(topic.name)

    standard_emitted: list[tuple[Destination, list[StandardEntry]]] = []
    omitted_documents: list[str] = []
    for destination in STANDARD_DOCUMENTS:
        members = [e for e in included_standard if e.group in destination.groups]
        if members:
            standard_emitted.append((destination, members))
        else:
            omitted_documents.append(destination.slug)

    home_document = {
        policy.id: (
            PRINCIPLES_DOCUMENT
            if policy.kind == "principle"
            else f"{home_topic[policy.id].slug}.md"
        )
        for policy in included
    }
    for destination, members in standard_emitted:
        for entry in members:
            home_document[entry.id] = f"{destination.slug}.md"
    for exemplar in admitted_exemplars:
        home_document[exemplar.id] = f"{EXEMPLARS.slug}.md"

    dropped: list[str] = []
    citations, demonstrated_by = _resolve_citations(
        admitted_exemplars,
        included_by_id,
        {e.id for e in included_standard},
        exclusions,
        dropped,
    )

    banner = _banner(config)
    standard_documents = {
        destination.slug: banner
        + _render_standard_document(
            config,
            destination.title,
            destination.groups,
            members,
            demonstrated_by,
            home_document,
            dropped,
        )
        for destination, members in standard_emitted
    }
    topic_documents = {
        topic.slug: banner
        + _render_topic_document(
            config,
            topic,
            ordered,
            included_by_id,
            home_topic,
            demonstrated_by,
            home_document,
            dropped,
        )
        for topic, ordered in emitted
    }
    written = {destination.slug for destination, _ in standard_emitted}
    if admitted_exemplars:
        written.add(EXEMPLARS.slug)
    entry, map_titles = _render_entry_document(
        config,
        identity,
        bool(principles),
        bool(admitted_exemplars),
        emitted,
        written,
    )
    triggered = sum(1 for _, ordered in emitted for p in ordered if p.trigger)
    triggerable = sum(len(ordered) for _, ordered in emitted)
    return Projection(
        entry=banner + entry,
        entry_name=entry_name,
        map_titles=map_titles,
        principles=(
            banner
            + _render_principles_document(config, principles, home_document, dropped)
            if principles
            else None
        ),
        topic_documents=topic_documents,
        standard_documents=standard_documents,
        exemplars=(
            banner
            + _render_exemplars_document(
                config, admitted_exemplars, citations, home_document, dropped
            )
            if admitted_exemplars
            else None
        ),
        sidecar=_render_sidecar(
            config,
            identity,
            principles,
            emitted,
            standard_emitted,
            admitted_exemplars,
            citations,
        ),
        identity=identity,
        omitted_topics=tuple(omitted),
        omitted_standard_documents=tuple(omitted_documents),
        dropped_references=tuple(dropped),
        trigger_coverage=(triggered, triggerable),
    )


def write(
    projection: Projection, admitted: list[Exemplar], out_dir: Path
) -> tuple[str, ...]:
    owned = (out_dir / "provenance.json").is_file()
    documents = projection.documents()

    out_dir.mkdir(parents=True, exist_ok=True)
    if owned:
        shutil.rmtree(out_dir / "exemplars", ignore_errors=True)
        for path in out_dir.glob("*.md"):
            if path.name not in documents:
                path.unlink()
    kept: list[str] = []
    for name, text in documents.items():
        if name in SEED_DOCUMENTS and (out_dir / name).is_file():
            kept.append(name)
            continue
        (out_dir / name).write_text(text, encoding="utf-8")
    for exemplar in admitted:
        destination = out_dir / "exemplars" / exemplar.directory.name
        try:
            shutil.copytree(
                exemplar.directory,
                destination,
                ignore=shutil.ignore_patterns("exemplar.md"),
            )
        except FileExistsError as exc:
            raise PolcError(
                [
                    f"{destination}: already present in an output directory "
                    "polc does not own"
                ]
            ) from exc
    (out_dir / "provenance.json").write_text(projection.sidecar, encoding="utf-8")
    return tuple(kept)
