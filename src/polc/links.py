from __future__ import annotations

import re
from dataclasses import dataclass

INLINE_LINK = re.compile(r"\[([^\]\n]*)\]\(([^)\s]*)\)")
CORPUS_TARGET = re.compile(r"((?:POL|STD|EXM)-\d{4})[^#]*\.md")
FENCE = re.compile(r" {0,3}(`{3,}|~{3,})")
BACKTICK_RUN = re.compile(r"`+")


@dataclass(frozen=True)
class Link:
    start: int
    end: int
    text: str
    path: str


def _code_spans(line: str) -> list[tuple[int, int]]:
    runs = [match.span() for match in BACKTICK_RUN.finditer(line)]
    spans: list[tuple[int, int]] = []
    index = 0
    while index < len(runs):
        start, end = runs[index]
        for closer in range(index + 1, len(runs)):
            other = runs[closer]
            if other[1] - other[0] == end - start:
                spans.append((start, other[1]))
                index = closer
                break
        index += 1
    return spans


def code_mask(text: str) -> list[bool]:
    mask = [False] * len(text)
    offset = 0
    fence: str | None = None
    for line in text.split("\n"):
        match = FENCE.match(line)
        if fence is None and match is None:
            for start, end in _code_spans(line):
                mask[offset + start : offset + end] = [True] * (end - start)
        else:
            mask[offset : offset + len(line)] = [True] * len(line)
            marker = match.group(1) if match is not None else None
            if fence is None:
                fence = marker
            elif (
                marker is not None
                and marker[0] == fence[0]
                and len(marker) >= len(fence)
                and not line[match.end() :].strip()
            ):
                fence = None
        offset += len(line) + 1
    return mask


def scan_links(text: str) -> list[Link]:
    mask = code_mask(text)
    links: list[Link] = []
    for match in INLINE_LINK.finditer(text):
        if mask[match.start()]:
            continue
        links.append(
            Link(
                start=match.start(),
                end=match.end(),
                text=match.group(1),
                path=match.group(2).partition("#")[0],
            )
        )
    return links
