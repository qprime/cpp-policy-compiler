import json


class TestSidecar:
    def test_every_rendered_policy_has_provenance_entry(self, ws):
        ws.standard_corpus()
        projection, _, _ = ws.project(domain="application")
        data = json.loads(projection.sidecar)
        assert set(data) == {
            "POL-0001", "POL-0002", "POL-0003", "POL-0004",
            "POL-0005", "POL-0006", "POL-0008",
        }
        assert data["POL-0001"]["topic"] == "tier1"
        entry = data["POL-0003"]
        assert entry["kind"] == "standard"
        assert entry["topic"] == "alpha-work"
        assert entry["statement"] == "Gamma standard"
        assert entry["attribution"] == [
            {"source": "testimony/notes.md", "locator": "S3", "upstream": ["CG X.1"]}
        ]
        assert entry["policy_file"] == "POL-0003-gamma-standard.md"

    def test_excluded_policy_absent_from_sidecar(self, ws):
        ws.standard_corpus()
        projection, _, _ = ws.project(domain="application")
        assert "POL-0007" not in json.loads(projection.sidecar)
