from __future__ import annotations

from pathlib import Path

from .corpus import parse_frontmatter
from .model import Budgets, Configuration, PolcError


def _required_int(value: object, origin: str, key: str, errors: list[str]) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"{origin}: '{key}' must be an integer")
        return 0
    return value


def _required_str(value: object, origin: str, key: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value:
        errors.append(f"{origin}: '{key}' must be a non-empty string")
        return ""
    return value


def load_configuration(path: Path) -> Configuration:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PolcError([f"{path}: cannot read configuration: {exc}"]) from exc
    frontmatter, _ = parse_frontmatter(text, path.name)

    errors: list[str] = []
    name = _required_str(frontmatter.get("name"), path.name, "name", errors)
    language_version = _required_int(
        frontmatter.get("language_version"), path.name, "language_version", errors
    )
    compiler = _required_str(frontmatter.get("compiler"), path.name, "compiler", errors)
    domain = _required_str(frontmatter.get("domain"), path.name, "domain", errors)

    budgets_raw = frontmatter.get("budgets")
    if not isinstance(budgets_raw, dict):
        errors.append(
            f"{path.name}: 'budgets' with entry_chars and topic_chars is required; "
            "the compiler has no defaults"
        )
        budgets = Budgets(0, 0)
    else:
        budgets = Budgets(
            _required_int(budgets_raw.get("entry_chars"), path.name, "budgets.entry_chars", errors),
            _required_int(budgets_raw.get("topic_chars"), path.name, "budgets.topic_chars", errors),
        )

    if errors:
        raise PolcError(errors)
    return Configuration(name, language_version, compiler, domain, budgets)
