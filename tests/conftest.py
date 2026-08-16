from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from polc.config import load_configuration
from polc.corpus import load_corpus
from polc.manifest import parse_manifest
from polc.render import render
from polc.select import select
from polc.validate import validate


def pytest_addoption(parser):
    parser.addoption("--update-goldens", action="store_true", default=False)


@pytest.fixture
def update_goldens(request):
    return request.config.getoption("--update-goldens")


class Workspace:
    def __init__(self, root: Path):
        self.root = root
        self.policies = root / "policies"
        self.policies.mkdir()

    def policy(
        self,
        policy_id,
        slug,
        kind,
        statement,
        body="A body paragraph.",
        filename=None,
        attribution=...,
        **frontmatter,
    ):
        fm = {"id": policy_id, "kind": kind}
        if attribution is ...:
            attribution = [{"source": "testimony/notes.md", "locator": "Section 1"}]
        if attribution is not None:
            fm["attribution"] = attribution
        fm.update(frontmatter)
        name = filename or f"{policy_id}-{slug}.md"
        text = (
            "---\n"
            + yaml.safe_dump(fm, sort_keys=True)
            + "---\n\n# "
            + statement
            + "\n\n"
            + body
            + "\n"
        )
        (self.policies / name).write_text(text, encoding="utf-8")

    def manifest(self, topics):
        lines = ["# Projection topics", "", "## Topics", ""]
        for name, read_when, members, cross_references in topics:
            lines += [f"### {name}", "", f"Read when: {read_when}", ""]
            if members:
                lines += [", ".join(members), ""]
            for target in cross_references:
                lines += [f"Cross-reference: {target} (homed elsewhere).", ""]
        (self.policies / "TOPICS.md").write_text("\n".join(lines), encoding="utf-8")

    def config(
        self,
        name="test-config",
        language_version=20,
        compiler="gcc",
        domain="application",
        budgets=...,
        filename="config.md",
    ):
        fm = {
            "name": name,
            "language_version": language_version,
            "compiler": compiler,
            "domain": domain,
        }
        if budgets is ...:
            budgets = {"entry_chars": 100000, "topic_chars": 100000}
        if budgets is not None:
            fm["budgets"] = budgets
        path = self.root / filename
        path.write_text("---\n" + yaml.safe_dump(fm, sort_keys=True) + "---\n", encoding="utf-8")
        return path

    def standard_corpus(self):
        self.policy("POL-0001", "alpha-principle", "principle", "Alpha principle", precedence=1)
        self.policy("POL-0002", "beta-principle", "principle", "Beta principle", precedence=2)
        self.policy(
            "POL-0003",
            "gamma-standard",
            "standard",
            "Gamma standard",
            attribution=[
                {"source": "testimony/notes.md", "locator": "S3", "upstream": ["CG X.1"]}
            ],
        )
        self.policy("POL-0004", "delta-guideline", "guideline", "Delta guideline")
        self.policy("POL-0005", "epsilon-pattern", "pattern", "Epsilon pattern")
        self.policy(
            "POL-0006", "zeta-never", "anti-pattern", "Never zeta", replacement=["POL-0005"]
        )
        self.policy(
            "POL-0007",
            "eta-realtime",
            "standard",
            "Eta realtime standard",
            applicability={"domain": ["realtime"]},
        )
        self.policy(
            "POL-0008", "theta-never", "anti-pattern", "Never theta", replacement=["POL-0001"]
        )
        self.manifest(
            [
                (
                    "Alpha work",
                    "doing alpha things.",
                    ["POL-0003", "POL-0004", "POL-0006", "POL-0005", "POL-0008"],
                    [],
                ),
                ("Gated work", "working under the gate.", ["POL-0007"], []),
            ]
        )

    def load(self):
        return load_corpus(self.policies), parse_manifest(self.policies / "TOPICS.md")

    def validate_errors(self, **config_kwargs):
        corpus, topics = self.load()
        config = load_configuration(self.config(**config_kwargs))
        return validate(corpus, topics, config)

    def project(self, **config_kwargs):
        corpus, topics = self.load()
        config = load_configuration(self.config(**config_kwargs))
        errors = validate(corpus, topics, config)
        assert errors == []
        included, exclusions = select(corpus, config)
        return render(topics, config, included), exclusions, config


@pytest.fixture
def ws(tmp_path):
    return Workspace(tmp_path)
