from __future__ import annotations

from dataclasses import replace

from .model import (
    Configuration,
    CorpusLayers,
    EffectiveCorpus,
    Exclusion,
    Exemplar,
    MergeDecision,
    Policy,
    PolcError,
    ProjectConfiguration,
    StandardEntry,
    Topic,
)


def _axis_value(config: Configuration, axis: str) -> str:
    return {
        "language_version": str(config.language_version),
        "compiler": config.compiler,
        "domain": config.domain,
    }[axis]


def excluding_axis(
    applicability: dict[str, tuple[str, ...]], config: Configuration
) -> str | None:
    return next(
        (
            axis
            for axis in sorted(applicability)
            if _axis_value(config, axis) not in applicability[axis]
        ),
        None,
    )


def select(
    corpus: list[Policy], config: Configuration
) -> tuple[list[Policy], list[Exclusion]]:
    included: list[Policy] = []
    exclusions: list[Exclusion] = []
    for policy in corpus:
        axis = excluding_axis(policy.applicability, config)
        if axis is None:
            included.append(policy)
        else:
            exclusions.append(Exclusion(policy.id, axis))

    by_id = {p.id: p for p in corpus}
    included_ids = {p.id for p in included}
    errors = [
        f"{policy.id}: anti-pattern is rendered but its replacement {target} "
        f"is excluded by applicability"
        for policy in included
        if policy.kind == "anti-pattern"
        for target in policy.replacement
        if target in by_id
        and by_id[target].kind != "principle"
        and target not in included_ids
    ]
    if errors:
        raise PolcError(errors)
    return included, exclusions


def select_standard(
    standard: list[StandardEntry], config: Configuration
) -> tuple[list[StandardEntry], list[Exclusion]]:
    included: list[StandardEntry] = []
    exclusions: list[Exclusion] = []
    for entry in standard:
        axis = excluding_axis(entry.applicability, config)
        if axis is None:
            included.append(entry)
        else:
            exclusions.append(Exclusion(entry.id, axis))
    return included, exclusions


def select_exemplars(
    exemplars: list[Exemplar], config: Configuration
) -> tuple[list[Exemplar], list[Exclusion]]:
    included: list[Exemplar] = []
    exclusions: list[Exclusion] = []
    for exemplar in exemplars:
        axis = excluding_axis(exemplar.applicability, config)
        if axis is None:
            included.append(exemplar)
        else:
            exclusions.append(Exclusion(exemplar.id, axis))
    return included, exclusions


def _merge_topics(upstream: list[Topic], local: list[Topic]) -> list[Topic]:
    merged = list(upstream)
    by_slug = {topic.slug: index for index, topic in enumerate(merged)}
    errors: list[str] = []
    for topic in local:
        index = by_slug.get(topic.slug)
        if index is None:
            by_slug[topic.slug] = len(merged)
            merged.append(topic)
            continue
        current = merged[index]
        if (
            topic.name != current.name
            or topic.read_when != current.read_when
            or topic.review_when != current.review_when
        ):
            errors.append(
                f"local topic '{topic.slug}' must keep upstream name, Read when, "
                "and Review when text"
            )
            continue
        merged[index] = replace(
            current,
            members=current.members + topic.members,
            cross_references=current.cross_references + topic.cross_references,
        )
    if errors:
        raise PolcError(errors)
    return merged


def _item_kind(item: Policy | StandardEntry | Exemplar) -> tuple[str, str | None]:
    if isinstance(item, Policy):
        return "policy", item.kind
    if isinstance(item, StandardEntry):
        return "standard", None
    return "exemplar", None


def build_effective_corpus(
    upstream: CorpusLayers,
    local: CorpusLayers,
    project: ProjectConfiguration,
) -> tuple[EffectiveCorpus, list[Exclusion]]:
    config = project.configuration
    policies, policy_axis_exclusions = select(list(upstream.policies), config)
    standard, standard_axis_exclusions = select_standard(list(upstream.standard), config)
    exemplars, exemplar_axis_exclusions = select_exemplars(
        list(upstream.exemplars), config
    )
    local_policies, local_policy_exclusions = select(list(local.policies), config)
    local_standard, local_standard_exclusions = select_standard(
        list(local.standard), config
    )
    local_exemplars, local_exemplar_exclusions = select_exemplars(
        list(local.exemplars), config
    )
    axis_exclusions = (
        policy_axis_exclusions
        + standard_axis_exclusions
        + exemplar_axis_exclusions
        + local_policy_exclusions
        + local_standard_exclusions
        + local_exemplar_exclusions
    )
    axis_excluded_ids = {exclusion.id for exclusion in axis_exclusions}

    upstream_items: dict[str, Policy | StandardEntry | Exemplar] = {
        item.id: item
        for item in upstream.policies + upstream.standard + upstream.exemplars
    }
    selected_upstream_ids = {
        item.id for item in policies + standard + exemplars
    }
    local_items: dict[str, Policy | StandardEntry | Exemplar] = {
        item.id: item for item in local_policies + local_standard + local_exemplars
    }
    errors: list[str] = []
    if len(local_items) != len(local_policies) + len(local_standard) + len(local_exemplars):
        errors.append("project overlay: duplicate local identity across corpus layers")

    topic_by_slug = {topic.slug: topic for topic in upstream.topics}
    excluded_topics: set[str] = set()
    excluded_ids: set[str] = set()
    decisions: list[MergeDecision] = []
    for exclusion in project.exclude_topics:
        if exclusion.topic in excluded_topics:
            errors.append(f"project.md: topic '{exclusion.topic}' is excluded more than once")
            continue
        topic = topic_by_slug.get(exclusion.topic)
        if topic is None:
            errors.append(f"project.md: excluded topic '{exclusion.topic}' does not resolve")
            continue
        excluded_topics.add(exclusion.topic)
        excluded_ids.update(topic.members)
        decisions.append(MergeDecision("exclude-topic", exclusion.topic, exclusion.reason))
        decisions.extend(
            MergeDecision("exclude-topic-member", member, exclusion.reason)
            for member in topic.members
        )
    for exclusion in project.exclude_ids:
        if exclusion.id not in upstream_items:
            errors.append(f"project.md: excluded id {exclusion.id} does not resolve upstream")
        if exclusion.id in excluded_ids:
            errors.append(f"project.md: id {exclusion.id} is excluded more than once")
        excluded_ids.add(exclusion.id)
        decisions.append(MergeDecision("exclude", exclusion.id, exclusion.reason))

    replacement_map: dict[str, str] = {}
    replacement_locals: set[str] = set()
    for replacement in project.replace_ids:
        upstream_item = upstream_items.get(replacement.upstream)
        local_item = local_items.get(replacement.local)
        if upstream_item is None:
            errors.append(
                f"project.md: replacement upstream {replacement.upstream} does not resolve"
            )
        elif replacement.upstream not in selected_upstream_ids:
            errors.append(
                f"project.md: replacement upstream {replacement.upstream} is excluded "
                "by applicability"
            )
        if local_item is None:
            errors.append(f"project.md: replacement local {replacement.local} does not resolve")
        if replacement.upstream in excluded_ids:
            errors.append(
                f"project.md: {replacement.upstream} cannot be both excluded and replaced"
            )
        if replacement.upstream in replacement_map:
            errors.append(f"project.md: {replacement.upstream} is replaced more than once")
        if replacement.local in replacement_locals:
            errors.append(f"project.md: local id {replacement.local} replaces more than one id")
        if (
            upstream_item is not None
            and local_item is not None
            and _item_kind(upstream_item) != _item_kind(local_item)
        ):
            errors.append(
                f"project.md: {replacement.local} is incompatible with {replacement.upstream}"
            )
        replacement_map[replacement.upstream] = replacement.local
        replacement_locals.add(replacement.local)
        decisions.append(
            MergeDecision(
                "replace", replacement.upstream, replacement.reason, replacement.local
            )
        )
    if errors:
        raise PolcError(errors)

    def retained(item: Policy | StandardEntry | Exemplar) -> bool:
        return item.id not in excluded_ids and item.id not in replacement_map

    effective_policies = [item for item in policies if retained(item)]
    effective_standard = [item for item in standard if retained(item)]
    effective_exemplars = [item for item in exemplars if retained(item)]
    effective_policies.extend(p for p in local_policies if p.id not in replacement_locals)
    effective_standard.extend(e for e in local_standard if e.id not in replacement_locals)
    effective_exemplars.extend(e for e in local_exemplars if e.id not in replacement_locals)
    for local_id in replacement_map.values():
        local_item = local_items[local_id]
        if isinstance(local_item, Policy):
            effective_policies.append(local_item)
        elif isinstance(local_item, StandardEntry):
            effective_standard.append(local_item)
        else:
            effective_exemplars.append(local_item)

    evidence_errors = [
        f"project.md: replacement {target} -> {replacement_map[target]} cannot "
        f"transfer exemplar evidence from {exemplar.id}; exclude {exemplar.id} or "
        "replace it with a compatible local exemplar that cites the local decision"
        for exemplar in effective_exemplars
        for target in exemplar.demonstrates
        if target in replacement_map
    ]
    if evidence_errors:
        raise PolcError(evidence_errors)

    effective_policies = [
        replace(
            policy,
            replacement=tuple(replacement_map.get(item, item) for item in policy.replacement),
        )
        for policy in effective_policies
    ]
    effective_exemplars = [
        replace(
            exemplar,
            demonstrates=tuple(
                item for item in exemplar.demonstrates
                if item not in axis_excluded_ids
            ),
        )
        for exemplar in effective_exemplars
    ]

    topics = _merge_topics(list(upstream.topics), list(local.topics))
    effective_topics: list[Topic] = []
    for topic in topics:
        if topic.slug in excluded_topics:
            continue
        effective_topics.append(
            replace(
                topic,
                members=tuple(
                    replacement_map.get(item, item)
                    for item in topic.members
                    if item not in excluded_ids and item not in axis_excluded_ids
                ),
                cross_references=tuple(
                    replacement_map.get(item, item)
                    for item in topic.cross_references
                    if item not in axis_excluded_ids
                ),
            )
        )
    standard_topic_ids = tuple(
        replacement_map.get(item, item)
        for item in upstream.standard_topic_ids
        if item not in excluded_ids and item not in axis_excluded_ids
    ) + tuple(e.id for e in local_standard if e.id not in replacement_locals)
    return EffectiveCorpus(
        tuple(effective_policies),
        tuple(effective_topics),
        tuple(effective_standard),
        standard_topic_ids,
        tuple(effective_exemplars),
        tuple(decisions),
    ), axis_exclusions
