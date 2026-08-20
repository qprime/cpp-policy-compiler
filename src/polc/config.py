from __future__ import annotations

from pathlib import Path

from .frontmatter import parse_frontmatter, required_str
from .model import Configuration, PolcError


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
