from __future__ import annotations

from pathlib import Path

from .frontmatter import parse_frontmatter, required_str
from .model import (
    Configuration,
    IdExclusion,
    IdReplacement,
    PolcError,
    ProjectConfiguration,
    TopicExclusion,
)

CONFIGURATION_KEYS = {"name", "language_version", "compiler", "domain"}
PROJECT_KEYS = CONFIGURATION_KEYS | {"exclude_topics", "exclude_ids", "replace_ids"}


def _required_int(value: object, origin: str, key: str, errors: list[str]) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"{origin}: '{key}' must be an integer")
        return 0
    return value


def load_configuration(path: Path) -> tuple[Configuration, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolcError([f"{path}: cannot read configuration: {exc}"]) from exc
    frontmatter, _ = parse_frontmatter(text, path.name)

    errors: list[str] = []
    name = required_str(frontmatter.get("name"), path.name, "name", errors)
    language_version = _required_int(
        frontmatter.get("language_version"), path.name, "language_version", errors
    )
    compiler = required_str(frontmatter.get("compiler"), path.name, "compiler", errors)
    domain = required_str(frontmatter.get("domain"), path.name, "domain", errors)

    if errors:
        raise PolcError(errors)
    return Configuration(name, language_version, compiler, domain), text


def _reasoned_records(
    value: object,
    origin: str,
    key: str,
    identity_key: str,
    errors: list[str],
) -> tuple[tuple[str, str], ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        errors.append(f"{origin}: '{key}' must be a list")
        return ()
    records: list[tuple[str, str]] = []
    for index, item in enumerate(value):
        item_origin = f"{origin}: {key}[{index}]"
        if not isinstance(item, dict) or set(item) != {identity_key, "reason"}:
            errors.append(
                f"{item_origin} must carry exactly '{identity_key}' and 'reason'"
            )
            continue
        identity = required_str(item.get(identity_key), item_origin, identity_key, errors)
        reason = required_str(item.get("reason"), item_origin, "reason", errors)
        if reason and not reason.strip():
            errors.append(f"{item_origin}: 'reason' must contain non-whitespace text")
            reason = ""
        if identity and reason:
            records.append((identity, reason))
    return tuple(records)


def _replacement_records(
    value: object, origin: str, errors: list[str]
) -> tuple[IdReplacement, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        errors.append(f"{origin}: 'replace_ids' must be a list")
        return ()
    records: list[IdReplacement] = []
    for index, item in enumerate(value):
        item_origin = f"{origin}: replace_ids[{index}]"
        if not isinstance(item, dict) or set(item) != {"upstream", "local", "reason"}:
            errors.append(
                f"{item_origin} must carry exactly 'upstream', 'local', and 'reason'"
            )
            continue
        upstream = required_str(item.get("upstream"), item_origin, "upstream", errors)
        local = required_str(item.get("local"), item_origin, "local", errors)
        reason = required_str(item.get("reason"), item_origin, "reason", errors)
        if reason and not reason.strip():
            errors.append(f"{item_origin}: 'reason' must contain non-whitespace text")
            reason = ""
        if upstream and local and reason:
            records.append(IdReplacement(upstream, local, reason))
    return tuple(records)


def load_project_configuration(path: Path) -> tuple[ProjectConfiguration, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolcError([f"{path}: cannot read project configuration: {exc}"]) from exc
    frontmatter, _ = parse_frontmatter(text, path.name)
    errors: list[str] = []
    unknown = sorted(frontmatter.keys() - PROJECT_KEYS)
    if unknown:
        errors.append(f"{path.name}: unknown frontmatter keys: {', '.join(unknown)}")
    name = required_str(frontmatter.get("name"), path.name, "name", errors)
    language_version = _required_int(
        frontmatter.get("language_version"), path.name, "language_version", errors
    )
    compiler = required_str(frontmatter.get("compiler"), path.name, "compiler", errors)
    domain = required_str(frontmatter.get("domain"), path.name, "domain", errors)
    topics = _reasoned_records(
        frontmatter.get("exclude_topics"),
        path.name,
        "exclude_topics",
        "topic",
        errors,
    )
    ids = _reasoned_records(
        frontmatter.get("exclude_ids"), path.name, "exclude_ids", "id", errors
    )
    replacements = _replacement_records(frontmatter.get("replace_ids"), path.name, errors)
    if errors:
        raise PolcError(errors)
    configuration = Configuration(name, language_version, compiler, domain)
    return ProjectConfiguration(
        configuration,
        tuple(TopicExclusion(topic, reason) for topic, reason in topics),
        tuple(IdExclusion(entry_id, reason) for entry_id, reason in ids),
        replacements,
    ), text
