from __future__ import annotations

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
    )


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
