from __future__ import annotations

import argparse
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from . import adapters
from .config import load_configuration, load_project_configuration
from .corpus import fingerprint, load_corpus, load_local_corpus, overlay_fingerprint
from .exemplars import load_exemplars, load_local_exemplars
from .evaluation import evaluate, write_result
from .manifest import parse_manifest, parse_standard_topics
from .model import (
    Configuration,
    CorpusLayers,
    Exclusion,
    Exemplar,
    Identity,
    PolcError,
    ProjectionMode,
)
from .render import Projection, render, write
from .select import build_effective_corpus, select, select_exemplars, select_standard
from .snapshot import record
from .standard import load_local_standard, load_standard
from .validate import validate, validate_links


def _build_projection(
    config_path: Path,
    policies_dir: Path,
    standard_dir: Path,
    exemplars_dir: Path,
    adapter: str | None,
    mode: ProjectionMode = ProjectionMode.GENERATION,
) -> tuple[Projection, list[Exclusion], Configuration, list[Exemplar]]:
    errors: list[str] = []
    corpus = topics = config = standard = standard_topic_ids = exemplars = None
    configuration_source = None
    try:
        corpus = load_corpus(policies_dir)
    except PolcError as exc:
        errors.extend(exc.errors)
    try:
        topics = parse_manifest(policies_dir / "TOPICS.md")
    except PolcError as exc:
        errors.extend(exc.errors)
    try:
        standard = load_standard(standard_dir)
    except PolcError as exc:
        errors.extend(exc.errors)
    try:
        standard_topic_ids = parse_standard_topics(policies_dir / "STANDARD-TOPICS.md")
    except PolcError as exc:
        errors.extend(exc.errors)
    try:
        exemplars = load_exemplars(exemplars_dir)
    except PolcError as exc:
        errors.extend(exc.errors)
    try:
        config, configuration_source = load_configuration(config_path)
    except PolcError as exc:
        errors.extend(exc.errors)
    if errors:
        raise PolcError(errors)

    errors = validate(corpus, topics, config, standard, standard_topic_ids, exemplars)
    if errors:
        raise PolcError(errors)

    included, exclusions = select(corpus, config)
    included_standard, standard_exclusions = select_standard(standard, config)
    admitted, exemplar_exclusions = select_exemplars(exemplars, config)
    all_exclusions = exclusions + standard_exclusions + exemplar_exclusions
    try:
        polc_version = version("polc")
    except PackageNotFoundError as exc:
        raise PolcError(
            [
                "distribution 'polc' is not installed, so its version cannot be "
                "recorded in the projection; install it (uv run polc, pip install -e .)"
            ]
        ) from exc
    identity = Identity(
        polc_version=polc_version,
        corpus_fingerprint=fingerprint(policies_dir, standard_dir, exemplars_dir),
        configuration_source=configuration_source,
        adapter=adapter,
    )
    projection = render(
        topics,
        config,
        included,
        included_standard,
        admitted,
        all_exclusions,
        entry_name=adapters.entry_name(adapter),
        identity=identity,
        mode=mode,
    )
    if not projection.topic_documents:
        raise PolcError(
            ["every topic omitted: the configuration excludes the whole policy corpus"]
        )
    projection = adapters.apply(adapter, projection, config)
    emitted_exemplars = admitted if mode == ProjectionMode.GENERATION else []
    errors = validate_links(projection, emitted_exemplars)
    if errors:
        raise PolcError(errors)
    return projection, all_exclusions, config, emitted_exemplars


def _build_project_projection(
    project_path: Path,
    policies_dir: Path,
    standard_dir: Path,
    exemplars_dir: Path,
    adapter: str | None,
    mode: ProjectionMode = ProjectionMode.GENERATION,
) -> tuple[Projection, list[Exclusion], Configuration, list[Exemplar]]:
    upstream_policies = load_corpus(policies_dir)
    upstream_topics = parse_manifest(policies_dir / "TOPICS.md")
    upstream_standard = load_standard(standard_dir)
    upstream_standard_topic_ids = parse_standard_topics(
        policies_dir / "STANDARD-TOPICS.md"
    )
    upstream_exemplars = load_exemplars(exemplars_dir)
    project, configuration_source = load_project_configuration(project_path)
    upstream_errors = validate(
        upstream_policies,
        upstream_topics,
        project.configuration,
        upstream_standard,
        upstream_standard_topic_ids,
        upstream_exemplars,
    )
    if upstream_errors:
        raise PolcError(upstream_errors)

    overlay_root = project_path.parent
    local_policies = load_local_corpus(overlay_root / "policies")
    local_topics_path = overlay_root / "policies" / "TOPICS.md"
    local_topics = parse_manifest(local_topics_path) if local_topics_path.is_file() else []
    local_standard = load_local_standard(overlay_root / "standard")
    local_exemplars = load_local_exemplars(overlay_root / "exemplars")
    effective, exclusions = build_effective_corpus(
        CorpusLayers(
            tuple(upstream_policies),
            tuple(upstream_topics),
            tuple(upstream_standard),
            tuple(upstream_standard_topic_ids),
            tuple(upstream_exemplars),
        ),
        CorpusLayers(
            tuple(local_policies),
            tuple(local_topics),
            tuple(local_standard),
            (),
            tuple(local_exemplars),
        ),
        project,
    )
    errors = validate(
        list(effective.policies),
        list(effective.topics),
        project.configuration,
        list(effective.standard),
        list(effective.standard_topic_ids),
        list(effective.exemplars),
    )
    if errors:
        raise PolcError(errors)
    try:
        polc_version = version("polc")
    except PackageNotFoundError as exc:
        raise PolcError(
            ["distribution 'polc' is not installed, so its version cannot be recorded"]
        ) from exc
    identity = Identity(
        polc_version=polc_version,
        corpus_fingerprint=fingerprint(policies_dir, standard_dir, exemplars_dir),
        configuration_source=configuration_source,
        adapter=adapter,
        overlay_fingerprint=overlay_fingerprint(project_path, overlay_root),
        decisions=effective.decisions,
    )
    projection = render(
        list(effective.topics),
        project.configuration,
        list(effective.policies),
        list(effective.standard),
        list(effective.exemplars),
        exclusions,
        entry_name=adapters.entry_name(adapter),
        identity=identity,
        mode=mode,
    )
    if not projection.topic_documents:
        raise PolcError(
            ["every topic omitted: the project overlay excludes the whole policy corpus"]
        )
    projection = adapters.apply(adapter, projection, project.configuration)
    emitted_exemplars = (
        list(effective.exemplars) if mode == ProjectionMode.GENERATION else []
    )
    errors = validate_links(projection, emitted_exemplars)
    if errors:
        raise PolcError(errors)
    return projection, exclusions, project.configuration, emitted_exemplars


def _report(projection: Projection, exclusions: list[Exclusion]) -> None:
    print(f"{projection.entry_name}: {len(projection.entry)} chars")
    if projection.principles is not None:
        print(f"principles.md: {len(projection.principles)} chars")
    for slug in sorted(projection.topic_documents):
        print(f"{slug}.md: {len(projection.topic_documents[slug])} chars")
    for slug, text in projection.standard_documents.items():
        print(f"{slug}.md: {len(text)} chars")
    if projection.exemplars is not None:
        print(f"exemplars.md: {len(projection.exemplars)} chars")
    print(f"configuration.md: {len(projection.identity.configuration_source)} chars")
    print(f"provenance.json: {len(projection.sidecar)} chars")
    for exclusion in exclusions:
        print(f"excluded {exclusion.id} ({exclusion.axis})")
    for name in projection.omitted_topics:
        print(f"omitted topic '{name}': every member excluded")
    for slug in projection.omitted_standard_documents:
        print(f"omitted {slug}.md: every entry excluded")
    if projection.exemplars is None:
        reason = (
            "review mode"
            if projection.mode == ProjectionMode.REVIEW
            else "every exemplar excluded"
        )
        print(f"omitted exemplars.md: {reason}")
    if projection.principles is None:
        print("omitted principles.md: every principle excluded")
    routed, routeable = projection.routing_coverage
    if routed < routeable:
        print(
            f"{routeable - routed} of {routeable} entries carry no "
            f"{projection.mode.value} route"
        )
    for line in projection.dropped_references:
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
        sub.add_argument("--standard", type=Path, default=Path("docs/standard"))
        sub.add_argument("--exemplars", type=Path, default=Path("docs/exemplars"))
        sub.add_argument(
            "--mode",
            choices=tuple(mode.value for mode in ProjectionMode),
            default=ProjectionMode.GENERATION.value,
        )
        if name == "build":
            sub.add_argument("--out", required=True, type=Path)
            sub.add_argument("--adapter", choices=adapters.ADAPTERS)
    eval_parser = subparsers.add_parser(
        "eval", help="run opt-in correctness evaluation"
    )
    eval_subparsers = eval_parser.add_subparsers(dest="eval_command", required=True)
    run_parser = eval_subparsers.add_parser(
        "run", help="evaluate a benchmark manifest"
    )
    run_parser.add_argument("manifest", type=Path)
    run_parser.add_argument("--out", required=True, type=Path)
    record_parser = eval_subparsers.add_parser(
        "record", help="record coherent file states while a command runs"
    )
    record_parser.add_argument("--root", required=True, type=Path)
    record_parser.add_argument("--path", action="append", required=True)
    record_parser.add_argument("--out", required=True, type=Path)
    record_parser.add_argument("--quiet-period-ms", type=int, default=500)
    record_parser.add_argument("command_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    if args.command == "eval":
        try:
            if args.eval_command == "run":
                result = evaluate(args.manifest)
                write_result(result, args.out)
                print(args.out)
            else:
                command = tuple(args.command_args)
                if command and command[0] == "--":
                    command = command[1:]
                manifest = record(
                    args.root,
                    tuple(args.path),
                    args.out,
                    command,
                    args.quiet_period_ms,
                )
                print(args.out / "recording.json")
                if manifest["exit_code"] != 0:
                    return int(manifest["exit_code"])
        except PolcError as exc:
            for message in exc.errors:
                print(message, file=sys.stderr)
            return 1
        return 0

    kept: tuple[str, ...] = ()
    try:
        projection, exclusions, _, admitted = _build_projection(
            args.config,
            args.policies,
            args.standard,
            args.exemplars,
            getattr(args, "adapter", None),
            ProjectionMode(args.mode),
        )
        if args.command == "build":
            kept = write(projection, admitted, args.out)
    except PolcError as exc:
        for message in exc.errors:
            print(message, file=sys.stderr)
        return 1

    _report(projection, exclusions)
    for name in kept:
        print(f"kept {name}: present and not owned")
    if args.command == "build":
        note = adapters.wiring_note(
            args.adapter, args.out, projection
        )
        if note is not None:
            print()
            print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
