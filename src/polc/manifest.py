from __future__ import annotations

import re
from pathlib import Path

from .model import PolcError, Topic

POLICY_ID = re.compile(r"POL-\d{4}(?!\d)")
STANDARD_ENTRY_LINK = re.compile(r"\[(STD-\d{4})\]\(")


def parse_standard_topics(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolcError([f"{path}: cannot read standard topics: {exc}"]) from exc
    ids = STANDARD_ENTRY_LINK.findall(text)
    if not ids:
        raise PolcError([f"{path.name}: no rows carry an entry link"])
    return ids


def _build_topic(
    name: str, paragraphs: list[str], origin: str, errors: list[str]
) -> Topic:
    read_when = None
    members: list[str] = []
    cross_references: list[str] = []
    for text in paragraphs:
        if text.startswith("Read when:"):
            read_when = text[len("Read when:") :].strip()
        elif text.startswith("Cross-reference:"):
            cross_references.extend(POLICY_ID.findall(text))
        else:
            members.extend(POLICY_ID.findall(text))
    if read_when is None:
        errors.append(f"{origin}: topic '{name}' has no 'Read when:' paragraph")
        read_when = ""
    if not members:
        errors.append(f"{origin}: topic '{name}' lists no members")
    slug = name.lower().replace(" ", "-")
    return Topic(name, slug, read_when, tuple(members), tuple(cross_references))


def parse_manifest(path: Path) -> list[Topic]:
    try:
        lines = path.read_text(encoding="utf-8").split("\n")
    except OSError as exc:
        raise PolcError([f"{path}: cannot read manifest: {exc}"]) from exc

    errors: list[str] = []
    topics: list[Topic] = []
    in_topics_section = False
    current_name: str | None = None
    paragraphs: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            paragraphs.append(" ".join(paragraph))
            paragraph = []

    def close_topic() -> None:
        nonlocal current_name, paragraphs
        flush_paragraph()
        if current_name is not None:
            topics.append(_build_topic(current_name, paragraphs, path.name, errors))
        current_name = None
        paragraphs = []

    for line in lines:
        if line.startswith("## "):
            close_topic()
            in_topics_section = line.strip() == "## Topics"
        elif line.startswith("### "):
            close_topic()
            if in_topics_section:
                current_name = line[4:].strip()
        elif current_name is not None:
            if line.strip():
                paragraph.append(line.strip())
            else:
                flush_paragraph()
    close_topic()

    if not topics:
        errors.append(f"{path.name}: no topics found under '## Topics'")
    if errors:
        raise PolcError(errors)
    return topics
