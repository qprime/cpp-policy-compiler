from __future__ import annotations

import re

from .model import (
    AXES,
    COMPILERS,
    KINDS,
    LANGUAGE_VERSIONS,
    Configuration,
    Policy,
    Topic,
)

CONFIG_LANGUAGE_VERSIONS = (14, 17, 20, 23)


def _validate_policies(corpus: list[Policy], by_id: dict[str, Policy], errors: list[str]) -> None:
    seen: dict[str, Policy] = {}
    for policy in corpus:
        if policy.id in seen:
            errors.append(
                f"{policy.path.name}: duplicate id {policy.id} "
                f"(also in {seen[policy.id].path.name})"
            )
        else:
            seen[policy.id] = policy

    for policy in corpus:
        origin = policy.path.name
        if not origin.startswith(policy.id + "-"):
            errors.append(f"{origin}: id {policy.id} does not match the filename prefix")
        if policy.kind not in KINDS:
            errors.append(f"{origin}: kind '{policy.kind}' is not one of {', '.join(KINDS)}")
        if not policy.attribution:
            errors.append(f"{origin}: attribution is required and non-empty")
        if policy.kind == "principle" and policy.precedence is None:
            errors.append(f"{origin}: principle without precedence")
        if policy.kind != "principle" and policy.precedence is not None:
            errors.append(f"{origin}: precedence appears on kind '{policy.kind}'")
        if policy.replacement and policy.kind != "anti-pattern":
            errors.append(f"{origin}: replacement appears on kind '{policy.kind}'")
        for target in policy.replacement:
            if target not in by_id:
                errors.append(f"{origin}: replacement {target} does not resolve")
        for axis, values in policy.applicability.items():
            if axis not in AXES:
                errors.append(f"{origin}: unknown applicability axis '{axis}'")
            elif axis == "language_version":
                for value in values:
                    if value not in LANGUAGE_VERSIONS:
                        errors.append(f"{origin}: illegal language_version mark '{value}'")
            elif axis == "compiler":
                for value in values:
                    if value not in COMPILERS:
                        errors.append(f"{origin}: illegal compiler mark '{value}'")

    precedences = sorted(
        p.precedence for p in corpus if p.kind == "principle" and p.precedence is not None
    )
    if precedences != list(range(1, len(precedences) + 1)):
        errors.append(
            f"principle precedence is not contiguous from 1: {precedences}"
        )


def _validate_topics(
    topics: list[Topic], by_id: dict[str, Policy], errors: list[str]
) -> dict[str, str]:
    membership: dict[str, str] = {}
    slugs: dict[str, str] = {}
    for topic in topics:
        if topic.slug in slugs:
            errors.append(
                f"topics '{slugs[topic.slug]}' and '{topic.name}' collide on slug '{topic.slug}'"
            )
        else:
            slugs[topic.slug] = topic.name
        for member in topic.members:
            if member in membership:
                if membership[member] == topic.name:
                    errors.append(f"{member}: listed twice in topic '{topic.name}'")
                else:
                    errors.append(
                        f"{member}: member of both '{membership[member]}' and '{topic.name}'"
                    )
            else:
                membership[member] = topic.name
            if member not in by_id:
                errors.append(f"topic '{topic.name}': member {member} does not resolve")
            elif by_id[member].kind == "principle":
                errors.append(
                    f"{member}: principle listed in topic '{topic.name}'; principles belong to no topic"
                )
        for target in topic.cross_references:
            if target not in by_id:
                errors.append(
                    f"topic '{topic.name}': cross-reference {target} does not resolve"
                )
            elif by_id[target].kind == "principle":
                errors.append(
                    f"topic '{topic.name}': cross-reference {target} targets a principle, "
                    "which is always loaded and has no home topic"
                )
    return membership


def _validate_anti_pattern_adjacency(
    corpus: list[Policy],
    by_id: dict[str, Policy],
    membership: dict[str, str],
    errors: list[str],
) -> None:
    for policy in corpus:
        if policy.kind != "anti-pattern":
            continue
        if not policy.replacement:
            errors.append(f"{policy.id}: anti-pattern with no replacement")
            continue
        non_principle = [
            r for r in policy.replacement if r in by_id and by_id[r].kind != "principle"
        ]
        if not non_principle:
            continue
        home = membership.get(policy.id)
        if home is not None and not any(membership.get(r) == home for r in non_principle):
            errors.append(
                f"{policy.id}: no non-principle replacement shares its topic '{home}'"
            )


def _validate_configuration(config: Configuration, errors: list[str]) -> None:
    origin = config.name or "configuration"
    if config.language_version not in CONFIG_LANGUAGE_VERSIONS:
        errors.append(
            f"{origin}: language_version {config.language_version} is not one of "
            f"{', '.join(str(v) for v in CONFIG_LANGUAGE_VERSIONS)}"
        )
    if config.compiler not in COMPILERS:
        errors.append(
            f"{origin}: compiler '{config.compiler}' is not one of {', '.join(COMPILERS)}"
        )
    if not re.fullmatch(r"\S+", config.domain or ""):
        errors.append(f"{origin}: domain must be a non-empty token")
    if config.budgets.entry_chars <= 0:
        errors.append(f"{origin}: budgets.entry_chars must be positive")
    if config.budgets.topic_chars <= 0:
        errors.append(f"{origin}: budgets.topic_chars must be positive")


def validate(
    corpus: list[Policy], topics: list[Topic], config: Configuration
) -> list[str]:
    errors: list[str] = []
    by_id = {p.id: p for p in corpus}

    _validate_policies(corpus, by_id, errors)
    membership = _validate_topics(topics, by_id, errors)
    for policy in corpus:
        if policy.kind != "principle" and policy.id not in membership:
            errors.append(f"{policy.id}: not a member of any topic")
    _validate_anti_pattern_adjacency(corpus, by_id, membership, errors)
    _validate_configuration(config, errors)
    return errors
