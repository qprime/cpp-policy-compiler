from __future__ import annotations

from .model import Configuration, Exclusion, Policy, PolcError


def _axis_value(config: Configuration, axis: str) -> str:
    return {
        "language_version": str(config.language_version),
        "compiler": config.compiler,
        "domain": config.domain,
    }[axis]


def select(
    corpus: list[Policy], config: Configuration
) -> tuple[list[Policy], list[Exclusion]]:
    included: list[Policy] = []
    exclusions: list[Exclusion] = []
    for policy in corpus:
        excluding_axis = next(
            (
                axis
                for axis in sorted(policy.applicability)
                if _axis_value(config, axis) not in policy.applicability[axis]
            ),
            None,
        )
        if excluding_axis is None:
            included.append(policy)
        else:
            exclusions.append(Exclusion(policy.id, excluding_axis))

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
