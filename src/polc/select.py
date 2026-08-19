from __future__ import annotations

from .model import (
    Configuration,
    Exclusion,
    Exemplar,
    Policy,
    PolcError,
    StandardEntry,
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
