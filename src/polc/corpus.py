from __future__ import annotations

import hashlib
from pathlib import Path

from .frontmatter import (
    parse_applicability,
    parse_attribution,
    parse_frontmatter,
    required_str,
    split_statement,
    string_list,
)
from .model import Policy, PolcError

POLICY_KEYS = {
    "id",
    "kind",
    "precedence",
    "applicability",
    "attribution",
    "replacement",
    "trigger",
    "review_trigger",
}


def _parse_policy(path: Path) -> Policy:
    frontmatter, markdown = parse_frontmatter(
        path.read_text(encoding="utf-8"), path.name
    )
    errors: list[str] = []

    unknown = sorted(frontmatter.keys() - POLICY_KEYS)
    if unknown:
        errors.append(f"{path.name}: unknown frontmatter keys: {', '.join(unknown)}")

    policy_id = required_str(frontmatter.get("id"), path.name, "id", errors)
    kind = required_str(frontmatter.get("kind"), path.name, "kind", errors)

    precedence = frontmatter.get("precedence")
    if precedence is not None and (isinstance(precedence, bool) or not isinstance(precedence, int)):
        errors.append(f"{path.name}: 'precedence' must be an integer")
        precedence = None

    attribution = parse_attribution(frontmatter.get("attribution"), path.name, errors)
    applicability = parse_applicability(frontmatter.get("applicability"), path.name, errors)
    replacement = (
        string_list(frontmatter["replacement"], path.name, "replacement", errors)
        if "replacement" in frontmatter
        else ()
    )
    trigger = (
        required_str(frontmatter["trigger"], path.name, "trigger", errors)
        if "trigger" in frontmatter
        else None
    )
    review_trigger = (
        required_str(
            frontmatter["review_trigger"], path.name, "review_trigger", errors
        )
        if "review_trigger" in frontmatter
        else None
    )
    try:
        statement, body = split_statement(markdown, path.name)
    except PolcError as exc:
        errors.extend(exc.errors)
        statement, body = "", ""

    if errors:
        raise PolcError(errors)
    return Policy(
        id=policy_id,
        kind=kind,
        statement=statement,
        body=body,
        attribution=attribution,
        path=path,
        precedence=precedence,
        applicability=applicability,
        replacement=replacement,
        trigger=trigger,
        review_trigger=review_trigger,
    )


def _fingerprint(contributions: list[tuple[str, Path]]) -> str:
    digest = hashlib.sha256()
    for key, path in sorted(contributions):
        digest.update(key.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return f"sha256:{digest.hexdigest()}"


def fingerprint(policies_dir: Path, standard_dir: Path, exemplars_dir: Path) -> str:
    contributions: list[tuple[str, Path]] = []
    roots = (
        ("policies", policies_dir),
        ("standard", standard_dir),
        ("exemplars", exemplars_dir),
    )
    for label, root in roots:
        for path in root.rglob("*"):
            if path.is_file():
                contributions.append(
                    (f"{label}/{path.relative_to(root).as_posix()}", path)
                )
    return _fingerprint(contributions)


def overlay_fingerprint(project_path: Path, overlay_root: Path) -> str:
    contributions = [("project.md", project_path)]
    for label in ("policies", "standard", "exemplars"):
        root = overlay_root / label
        for path in root.rglob("*") if root.is_dir() else ():
            if path.is_file():
                contributions.append(
                    (f"{label}/{path.relative_to(root).as_posix()}", path)
                )
    return _fingerprint(contributions)


def load_corpus(policies_dir: Path) -> list[Policy]:
    errors: list[str] = []
    policies: list[Policy] = []
    paths = sorted(policies_dir.glob("POL-*.md"))
    if not paths:
        raise PolcError([f"{policies_dir}: no policy files found"])
    for path in paths:
        try:
            policies.append(_parse_policy(path))
        except PolcError as exc:
            errors.extend(exc.errors)
    if errors:
        raise PolcError(errors)
    return policies


def load_local_corpus(policies_dir: Path) -> list[Policy]:
    if not policies_dir.is_dir():
        return []
    errors: list[str] = []
    policies: list[Policy] = []
    for path in sorted(policies_dir.glob("PRJ-POL-*.md")):
        try:
            policies.append(_parse_policy(path))
        except PolcError as exc:
            errors.extend(exc.errors)
    unexpected = sorted(p.name for p in policies_dir.glob("POL-*.md"))
    if unexpected:
        errors.append(
            f"{policies_dir}: local policy files must use PRJ-POL ids: "
            f"{', '.join(unexpected)}"
        )
    if errors:
        raise PolcError(errors)
    return policies
