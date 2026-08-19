from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .model import (
    STANDARD_DOCUMENTS,
    Configuration,
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


@dataclass(frozen=True)
class Projection:
    entry: str
    topic_documents: dict[str, str]
    standard_documents: dict[str, str]
    sidecar: str
    omitted_topics: tuple[str, ...]
    omitted_standard_documents: tuple[str, ...]
    dropped_cross_references: tuple[str, ...]


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


def _entry_block(heading: str, reference: str, body: str) -> list[str]:
    return [heading, "", reference, "", body, ""]


def _render_entry_document(
    config: Configuration,
    principles: list[Policy],
    emitted: list[tuple[Topic, list[Policy]]],
) -> str:
    lines = [
        f"# {config.name}",
        "",
        f"- Standard: C++{config.language_version}",
        f"- Compiler: {config.compiler}",
        f"- Domain: {config.domain}",
        "",
        "Per-standard tables in these documents read against the declared standard above.",
        "",
    ]
    for principle in principles:
        lines.extend(
            _entry_block(
                f"## {principle.statement}", _compact_ref(principle), principle.body
            )
        )
    lines.append("## Map")
    lines.append("")
    for topic, _ in emitted:
        lines.append(f"- [{topic.name}]({topic.slug}.md) — {topic.read_when}")
    return "\n".join(lines).rstrip("\n") + "\n"


def _render_topic_document(
    config: Configuration,
    topic: Topic,
    ordered: list[Policy],
    included_by_id: dict[str, Policy],
    home_topic: dict[str, Topic],
    dropped: list[str],
) -> str:
    lines = [
        f"{config.name} › {topic.name}",
        "",
        f"Read when: {topic.read_when}",
        "",
    ]
    for policy in ordered:
        lines.extend(
            _entry_block(
                f"## {MARKS[policy.kind]} — {policy.statement}",
                _compact_ref(policy),
                policy.body,
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
) -> str:
    lines = [f"{config.name} › {title}", ""]
    for group in groups:
        grouped = sorted((e for e in members if e.group == group), key=lambda e: e.id)
        if not grouped:
            continue
        lines.extend([f"## {_group_heading(group)}", ""])
        for entry in grouped:
            lines.extend(
                _entry_block(f"### {entry.statement}", _standard_ref(entry), entry.body)
            )
    return "\n".join(lines).rstrip("\n") + "\n"


def _attribution_records(item: Policy | StandardEntry) -> list[dict[str, object]]:
    return [
        {"source": a.source, "locator": a.locator, "upstream": list(a.upstream)}
        for a in item.attribution
    ]


def _render_sidecar(
    principles: list[Policy],
    emitted: list[tuple[Topic, list[Policy]]],
    standard: list[tuple[str, list[StandardEntry]]],
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
        record(principle, "tier1")
    for topic, ordered in emitted:
        for policy in ordered:
            record(policy, topic.slug)
    for slug, members in standard:
        for entry in members:
            entries[entry.id] = {
                "layer": "standard",
                "group": entry.group,
                "enforced_by": entry.enforced_by,
                "document": f"{slug}.md",
                "statement": entry.statement,
                "attribution": _attribution_records(entry),
                "file": entry.path.name,
            }
    data = {entry_id: entries[entry_id] for entry_id in sorted(entries)}
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render(
    topics: list[Topic],
    config: Configuration,
    included: list[Policy],
    included_standard: list[StandardEntry],
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

    standard_emitted: list[tuple[str, list[StandardEntry]]] = []
    omitted_documents: list[str] = []
    standard_documents: dict[str, str] = {}
    for slug, title, groups in STANDARD_DOCUMENTS:
        members = [e for e in included_standard if e.group in groups]
        if not members:
            omitted_documents.append(slug)
            continue
        standard_emitted.append((slug, members))
        standard_documents[slug] = _render_standard_document(
            config, title, groups, members
        )

    dropped: list[str] = []
    topic_documents = {
        topic.slug: _render_topic_document(
            config, topic, ordered, included_by_id, home_topic, dropped
        )
        for topic, ordered in emitted
    }
    return Projection(
        entry=_render_entry_document(config, principles, emitted),
        topic_documents=topic_documents,
        standard_documents=standard_documents,
        sidecar=_render_sidecar(principles, emitted, standard_emitted),
        omitted_topics=tuple(omitted),
        omitted_standard_documents=tuple(omitted_documents),
        dropped_cross_references=tuple(dropped),
    )


def write(projection: Projection, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.md").write_text(projection.entry, encoding="utf-8")
    for slug, text in projection.topic_documents.items():
        (out_dir / f"{slug}.md").write_text(text, encoding="utf-8")
    for slug, text in projection.standard_documents.items():
        (out_dir / f"{slug}.md").write_text(text, encoding="utf-8")
    (out_dir / "provenance.json").write_text(projection.sidecar, encoding="utf-8")
