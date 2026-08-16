import pytest

from polc.corpus import load_corpus
from polc.model import Attribution, PolcError


class TestCorpusLoading:
    def test_parses_frontmatter_statement_and_body(self, ws):
        ws.policy(
            "POL-0001",
            "alpha",
            "standard",
            "Alpha statement",
            body="First paragraph.\n\nSecond paragraph.",
            attribution=[
                {"source": "testimony/notes.md", "locator": "L1", "upstream": ["CG A.1"]}
            ],
            applicability={"domain": ["realtime"]},
        )
        [policy] = load_corpus(ws.policies)
        assert policy.id == "POL-0001"
        assert policy.kind == "standard"
        assert policy.statement == "Alpha statement"
        assert policy.body == "First paragraph.\n\nSecond paragraph."
        assert policy.attribution == (
            Attribution("testimony/notes.md", "L1", ("CG A.1",)),
        )
        assert policy.applicability == {"domain": ("realtime",)}
        assert policy.replacement == ()

    def test_reports_all_malformed_files_not_just_first(self, ws):
        (ws.policies / "POL-0001-bad.md").write_text("no frontmatter here\n")
        (ws.policies / "POL-0002-bad.md").write_text(
            "---\nid: [unclosed\n---\n\n# Statement\n"
        )
        with pytest.raises(PolcError) as excinfo:
            load_corpus(ws.policies)
        assert len(excinfo.value.errors) == 2
        assert any("POL-0001-bad.md" in e for e in excinfo.value.errors)
        assert any("POL-0002-bad.md" in e for e in excinfo.value.errors)

    def test_rejects_second_h1(self, ws):
        ws.policy(
            "POL-0001",
            "alpha",
            "standard",
            "Alpha statement",
            body="Some text.\n\n# A second decision\n\nMore text.",
        )
        with pytest.raises(PolcError) as excinfo:
            load_corpus(ws.policies)
        assert any("exactly one H1" in e for e in excinfo.value.errors)
