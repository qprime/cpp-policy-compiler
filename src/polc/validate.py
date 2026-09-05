from __future__ import annotations

import re

from .links import code_mask, scan_links
from .model import (
    AXES,
    COMPILERS,
    ENFORCERS,
    KINDS,
    LANGUAGE_VERSIONS,
    RESERVED_SLUGS,
    STANDARD_GROUPS,
    Configuration,
    Exemplar,
    Policy,
    StandardEntry,
    Topic,
)
from .render import Projection

CONFIG_LANGUAGE_VERSIONS = (14, 17, 20, 23)
STANDARD_TOPICS = "STANDARD-TOPICS.md"
DEMONSTRATED_ID = re.compile(r"(?:(?:PRJ-)?POL|(?:PRJ-)?STD)-\d{4}")
URL_SCHEME = re.compile(r"[a-z][a-z0-9+.-]*:|//", re.IGNORECASE)


def _validate_applicability(
    origin: str, applicability: dict[str, tuple[str, ...]], errors: list[str]
) -> None:
    for axis, values in applicability.items():
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


def _validate_trigger(origin: str, policy: Policy, errors: list[str]) -> None:
    if policy.trigger is None:
        return
    if policy.kind == "principle":
        errors.append(
            f"{origin}: trigger appears on a principle, which has no topic document "
            "to hold the row"
        )
    trigger = policy.trigger.strip()
    if not trigger:
        errors.append(f"{origin}: 'trigger' must be a non-empty string")
        return
    if trigger.endswith("."):
        errors.append(
            f"{origin}: trigger ends with a period; it is a fragment completing "
            "'when you are about to'"
        )
    if trigger[0].isupper():
        errors.append(
            f"{origin}: trigger opens with a capital; it is a fragment completing "
            "'when you are about to'"
        )


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
        _validate_trigger(origin, policy, errors)
        _validate_applicability(origin, policy.applicability, errors)

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
        if topic.slug in RESERVED_SLUGS:
            errors.append(
                f"topic '{topic.name}': slug '{topic.slug}' collides with a rendered document"
            )
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


def _validate_standard(
    standard: list[StandardEntry], topic_ids: list[str], errors: list[str]
) -> None:
    seen: dict[str, StandardEntry] = {}
    for entry in standard:
        if entry.id in seen:
            errors.append(
                f"{entry.path.name}: duplicate id {entry.id} "
                f"(also in {seen[entry.id].path.name})"
            )
        else:
            seen[entry.id] = entry

    for entry in standard:
        origin = entry.path.name
        if not origin.startswith(entry.id + "-"):
            errors.append(f"{origin}: id {entry.id} does not match the filename prefix")
        if entry.group not in STANDARD_GROUPS:
            errors.append(
                f"{origin}: group '{entry.group}' is not one of {', '.join(STANDARD_GROUPS)}"
            )
        if entry.enforced_by not in ENFORCERS:
            errors.append(
                f"{origin}: enforced_by '{entry.enforced_by}' is not one of "
                f"{', '.join(ENFORCERS)}"
            )
        if not entry.attribution:
            errors.append(f"{origin}: attribution is required and non-empty")
        _validate_applicability(origin, entry.applicability, errors)

    placed: set[str] = set()
    for entry_id in topic_ids:
        if entry_id in placed:
            errors.append(f"{STANDARD_TOPICS}: {entry_id} is placed in more than one row")
        placed.add(entry_id)
    for entry_id in sorted(placed - seen.keys()):
        errors.append(f"{STANDARD_TOPICS}: {entry_id} does not resolve to an entry")
    for entry_id in sorted(seen.keys() - placed):
        errors.append(f"{entry_id}: no linked row in {STANDARD_TOPICS}")


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


def _validate_demonstrates(
    origin: str,
    exemplar: Exemplar,
    by_id: dict[str, Policy],
    standard_by_id: dict[str, StandardEntry],
    errors: list[str],
) -> None:
    if not exemplar.demonstrates:
        errors.append(f"{origin}: 'demonstrates' is required and non-empty")
    for target in exemplar.demonstrates:
        if not DEMONSTRATED_ID.fullmatch(target):
            errors.append(f"{origin}: demonstrates entry '{target}' is not an id")
        elif target.startswith("POL-"):
            policy = by_id.get(target)
            if policy is None:
                errors.append(f"{origin}: demonstrates {target} does not resolve")
            elif policy.kind == "anti-pattern":
                errors.append(
                    f"{origin}: demonstrates {target}, which is an anti-pattern; "
                    "an exemplar is code to write"
                )
        elif target not in standard_by_id:
            errors.append(f"{origin}: demonstrates {target} does not resolve")


def _validate_neighbours(origin: str, exemplar: Exemplar, errors: list[str]) -> None:
    present = {source.as_posix() for source in exemplar.sources}
    if not any(source.name.endswith("_test.cpp") for source in exemplar.sources):
        errors.append(f"{origin}: no test file in the tree")
    for source in exemplar.sources:
        if source.suffix != ".cpp" or source.stem.endswith("_test"):
            continue
        test = source.with_name(f"{source.stem}_test.cpp").as_posix()
        if test not in present:
            errors.append(f"{origin}: {source.as_posix()} has no {test} beside it")
        header = source.with_suffix(".hpp").as_posix()
        if header not in present and not any(
            path.match(f"include/*/{header}") for path in exemplar.sources
        ):
            errors.append(f"{origin}: {source.as_posix()} has no declaring header")


def _validate_body_headings(origin: str, body: str, errors: list[str]) -> None:
    mask = code_mask(body)
    offset = 0
    for line in body.split("\n"):
        if re.match(r"#{1,2} ", line) and not mask[offset]:
            errors.append(
                f"{origin}: body heading '{line.strip()}' sits at the level the "
                "statement renders into; use '###' or deeper"
            )
        offset += len(line) + 1


def _validate_exemplars(
    exemplars: list[Exemplar],
    by_id: dict[str, Policy],
    standard_by_id: dict[str, StandardEntry],
    errors: list[str],
) -> None:
    seen: dict[str, Exemplar] = {}
    for exemplar in exemplars:
        if exemplar.id in seen:
            errors.append(
                f"{exemplar.directory.name}: duplicate id {exemplar.id} "
                f"(also in {seen[exemplar.id].directory.name})"
            )
        else:
            seen[exemplar.id] = exemplar

    for exemplar in exemplars:
        origin = f"{exemplar.directory.name}/exemplar.md"
        if not exemplar.directory.name.startswith(exemplar.id + "-"):
            errors.append(
                f"{origin}: id {exemplar.id} does not match the directory prefix"
            )
        if not exemplar.situation.strip():
            errors.append(f"{origin}: 'situation' must be a non-empty string")
        _validate_demonstrates(origin, exemplar, by_id, standard_by_id, errors)
        _validate_applicability(origin, exemplar.applicability, errors)
        _validate_body_headings(origin, exemplar.body, errors)
        _validate_neighbours(origin, exemplar, errors)


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


def validate(
    corpus: list[Policy],
    topics: list[Topic],
    config: Configuration,
    standard: list[StandardEntry],
    standard_topic_ids: list[str],
    exemplars: list[Exemplar],
) -> list[str]:
    errors: list[str] = []
    by_id = {p.id: p for p in corpus}
    standard_by_id = {e.id: e for e in standard}

    _validate_policies(corpus, by_id, errors)
    _validate_standard(standard, standard_topic_ids, errors)
    _validate_exemplars(exemplars, by_id, standard_by_id, errors)
    membership = _validate_topics(topics, by_id, errors)
    for policy in corpus:
        if policy.kind != "principle" and policy.id not in membership:
            errors.append(f"{policy.id}: not a member of any topic")
    _validate_anti_pattern_adjacency(corpus, by_id, membership, errors)
    _validate_configuration(config, errors)
    return errors


def _emitted_paths(projection: Projection, admitted: list[Exemplar]) -> set[str]:
    paths = set(projection.documents()) | {"provenance.json"}
    for exemplar in admitted:
        root = f"exemplars/{exemplar.directory.name}"
        paths.add(f"{root}/")
        for source in exemplar.sources:
            paths.add(f"{root}/{source.as_posix()}")
            for parent in source.parents:
                if parent.as_posix() != ".":
                    paths.add(f"{root}/{parent.as_posix()}/")
    return paths


def validate_links(projection: Projection, admitted: list[Exemplar]) -> list[str]:
    emitted = _emitted_paths(projection, admitted)

    errors: list[str] = []
    for name, text in projection.documents().items():
        for link in scan_links(text):
            if not link.path or URL_SCHEME.match(link.path):
                continue
            if link.path not in emitted and f"{link.path}/" not in emitted:
                errors.append(
                    f"{name}: link target '{link.path}' resolves to no emitted path"
                )
    return errors
