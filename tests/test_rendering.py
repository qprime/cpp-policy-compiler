import re
from pathlib import Path

from polc.config import load_configuration
from polc.corpus import load_corpus
from polc.manifest import parse_manifest
from polc.render import render
from polc.select import select

REPO = Path(__file__).resolve().parent.parent

REF_LINE = re.compile(r"^(POL-\d{4})(?!\d)(?: · [^\n]*)?$", re.MULTILINE)


def _real_projection():
    corpus = load_corpus(REPO / "docs" / "policies")
    topics = parse_manifest(REPO / "docs" / "policies" / "TOPICS.md")
    config = load_configuration(
        REPO / "docs" / "configurations" / "cpp20-gcc-application.md"
    )
    included, exclusions = select(corpus, config)
    return render(topics, config, included), exclusions


class TestRendering:
    def test_anti_pattern_follows_latest_replacement(self):
        projection, _ = _real_projection()
        ids = REF_LINE.findall(projection.topic_documents["choosing-a-representation"])
        assert ids.index("POL-0044") == ids.index("POL-0037") + 1

        ids = REF_LINE.findall(projection.topic_documents["writing-a-function"])
        assert ids.index("POL-0046") == ids.index("POL-0035") + 1
        assert ids.index("POL-0047") == ids.index("POL-0046") + 1

    def test_marks_match_kind(self, ws):
        ws.standard_corpus()
        projection, _, _ = ws.project()
        doc = projection.topic_documents["alpha-work"]
        assert "## MUST — Gamma standard" in doc
        assert "## SHOULD — Delta guideline" in doc
        assert "## THIS WAY — Epsilon pattern" in doc
        assert "## NEVER — Never zeta" in doc

    def test_principles_render_in_precedence_order_in_entry_doc(self, ws):
        ws.policy("POL-0001", "alpha-principle", "principle", "Alpha principle", precedence=2)
        ws.policy("POL-0002", "beta-principle", "principle", "Beta principle", precedence=1)
        ws.policy("POL-0003", "gamma-standard", "standard", "Gamma standard")
        ws.manifest([("Alpha work", "doing alpha things.", ["POL-0003"], [])])
        projection, _, _ = ws.project()
        assert (
            projection.entry.index("## Beta principle")
            < projection.entry.index("## Alpha principle")
        )

    def test_filtered_topic_absent_from_map(self, ws):
        ws.standard_corpus()
        projection, _, _ = ws.project(domain="application")
        assert "Gated work" not in projection.entry
        assert "gated-work" not in projection.topic_documents
        assert projection.omitted_topics == ("Gated work",)

    def test_cross_reference_dropped_when_target_excluded(self, ws):
        ws.standard_corpus()
        ws.manifest(
            [("Alpha work", "doing alpha things.",
              ["POL-0003", "POL-0004", "POL-0005", "POL-0006", "POL-0008"], ["POL-0007"]),
             ("Gated work", "working under the gate.", ["POL-0007"], [])]
        )
        projection, _, _ = ws.project(domain="realtime")
        assert "See also:" in projection.topic_documents["alpha-work"]

        projection, _, _ = ws.project(domain="application")
        assert "See also:" not in projection.topic_documents["alpha-work"]
        assert any("POL-0007" in d for d in projection.dropped_cross_references)

    def test_output_byte_identical_across_two_runs(self):
        first, _ = _real_projection()
        second, _ = _real_projection()
        assert first.entry == second.entry
        assert first.topic_documents == second.topic_documents
        assert first.sidecar == second.sidecar
