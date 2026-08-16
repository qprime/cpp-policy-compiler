import pytest

from polc.config import load_configuration
from polc.model import Exclusion, PolcError
from polc.select import select


class TestSelection:
    def test_domain_gated_policy_included_when_domain_matches(self, ws):
        ws.standard_corpus()
        corpus, _ = ws.load()
        config = load_configuration(ws.config(domain="realtime"))
        included, exclusions = select(corpus, config)
        assert "POL-0007" in {p.id for p in included}
        assert exclusions == []

    def test_domain_gated_policy_excluded_otherwise(self, ws):
        ws.standard_corpus()
        corpus, _ = ws.load()
        config = load_configuration(ws.config(domain="application"))
        included, exclusions = select(corpus, config)
        assert "POL-0007" not in {p.id for p in included}
        assert exclusions == [Exclusion("POL-0007", "domain")]

    def test_unknown_applicability_axis_fails(self, ws):
        ws.standard_corpus()
        ws.policy(
            "POL-0009", "iota-standard", "standard", "Iota standard",
            applicability={"platform": ["x86"]},
        )
        ws.manifest(
            [("Alpha work", "doing alpha things.",
              ["POL-0003", "POL-0004", "POL-0005", "POL-0006", "POL-0008", "POL-0009"], []),
             ("Gated work", "working under the gate.", ["POL-0007"], [])]
        )
        errors = ws.validate_errors()
        assert any("unknown applicability axis 'platform'" in e for e in errors)

    def test_excluded_replacement_with_rendered_anti_pattern_fails(self, ws):
        ws.policy("POL-0001", "alpha-principle", "principle", "Alpha principle", precedence=1)
        ws.policy(
            "POL-0002", "beta-pattern", "pattern", "Beta pattern",
            applicability={"domain": ["realtime"]},
        )
        ws.policy(
            "POL-0003", "gamma-never", "anti-pattern", "Never gamma",
            replacement=["POL-0002"],
        )
        ws.manifest([("Alpha work", "doing alpha things.", ["POL-0002", "POL-0003"], [])])
        corpus, _ = ws.load()
        config = load_configuration(ws.config(domain="application"))
        with pytest.raises(PolcError) as excinfo:
            select(corpus, config)
        assert any(
            "POL-0003" in e and "POL-0002" in e and "excluded" in e
            for e in excinfo.value.errors
        )
