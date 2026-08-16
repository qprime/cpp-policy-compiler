from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import load_configuration
from .corpus import load_corpus
from .manifest import parse_manifest
from .model import Configuration, Exclusion, PolcError
from .render import Projection, render, write
from .select import select
from .validate import validate


def _build_projection(
    config_path: Path, policies_dir: Path
) -> tuple[Projection, list[Exclusion], Configuration]:
    errors: list[str] = []
    corpus = topics = config = None
    try:
        corpus = load_corpus(policies_dir)
    except PolcError as exc:
        errors.extend(exc.errors)
    try:
        topics = parse_manifest(policies_dir / "TOPICS.md")
    except PolcError as exc:
        errors.extend(exc.errors)
    try:
        config = load_configuration(config_path)
    except PolcError as exc:
        errors.extend(exc.errors)
    if errors:
        raise PolcError(errors)

    errors = validate(corpus, topics, config)
    if errors:
        raise PolcError(errors)

    included, exclusions = select(corpus, config)
    return render(topics, config, included), exclusions, config


def _report(projection: Projection, exclusions: list[Exclusion]) -> None:
    print(f"index.md: {len(projection.entry)} chars")
    for slug in sorted(projection.topic_documents):
        print(f"{slug}.md: {len(projection.topic_documents[slug])} chars")
    print(f"provenance.json: {len(projection.sidecar)} chars")
    for exclusion in exclusions:
        print(f"excluded {exclusion.policy_id} ({exclusion.axis})")
    for name in projection.omitted_topics:
        print(f"omitted topic '{name}': every member excluded")
    for line in projection.dropped_cross_references:
        print(f"dropped {line}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="polc", description="Project the policy corpus through a configuration"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("build", "validate, render, and write a projection"),
        ("check", "validate and render; write nothing"),
    ):
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("--config", required=True, type=Path)
        sub.add_argument("--policies", type=Path, default=Path("docs/policies"))
        if name == "build":
            sub.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)

    try:
        projection, exclusions, _ = _build_projection(args.config, args.policies)
    except PolcError as exc:
        for message in exc.errors:
            print(message, file=sys.stderr)
        return 1

    if args.command == "build":
        write(projection, args.out)
    _report(projection, exclusions)
    return 0


if __name__ == "__main__":
    sys.exit(main())
