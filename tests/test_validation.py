class TestValidation:
    def test_precedence_gap_fails(self, ws):
        ws.standard_corpus()
        ws.policy("POL-0009", "iota-principle", "principle", "Iota principle", precedence=4)
        errors = ws.validate_errors()
        assert any("not contiguous" in e for e in errors)

    def test_precedence_on_non_principle_fails(self, ws):
        ws.standard_corpus()
        ws.policy("POL-0009", "iota-standard", "standard", "Iota standard", precedence=3)
        errors = ws.validate_errors()
        assert any("precedence appears on kind 'standard'" in e for e in errors)

    def test_replacement_on_non_anti_pattern_fails(self, ws):
        ws.standard_corpus()
        ws.policy(
            "POL-0009", "iota-guideline", "guideline", "Iota guideline",
            replacement=["POL-0005"],
        )
        errors = ws.validate_errors()
        assert any("replacement appears on kind 'guideline'" in e for e in errors)

    def test_dangling_replacement_fails(self, ws):
        ws.standard_corpus()
        ws.policy(
            "POL-0009", "iota-never", "anti-pattern", "Never iota",
            replacement=["POL-0099"],
        )
        errors = ws.validate_errors()
        assert any("replacement POL-0099 does not resolve" in e for e in errors)

    def test_orphan_policy_fails(self, ws):
        ws.standard_corpus()
        ws.policy("POL-0009", "iota-standard", "standard", "Iota standard")
        errors = ws.validate_errors()
        assert any("POL-0009: not a member of any topic" in e for e in errors)

    def test_unknown_manifest_id_fails(self, ws):
        ws.standard_corpus()
        ws.manifest(
            [("Alpha work", "doing alpha things.",
              ["POL-0003", "POL-0004", "POL-0005", "POL-0006", "POL-0008", "POL-0099"], []),
             ("Gated work", "working under the gate.", ["POL-0007"], [])]
        )
        errors = ws.validate_errors()
        assert any("member POL-0099 does not resolve" in e for e in errors)

    def test_duplicate_membership_fails(self, ws):
        ws.standard_corpus()
        ws.manifest(
            [("Alpha work", "doing alpha things.",
              ["POL-0003", "POL-0004", "POL-0005", "POL-0006", "POL-0008"], []),
             ("Gated work", "working under the gate.", ["POL-0007", "POL-0003"], [])]
        )
        errors = ws.validate_errors()
        assert any("member of both 'Alpha work' and 'Gated work'" in e for e in errors)

    def test_principle_in_topic_fails(self, ws):
        ws.standard_corpus()
        ws.manifest(
            [("Alpha work", "doing alpha things.",
              ["POL-0001", "POL-0003", "POL-0004", "POL-0005", "POL-0006", "POL-0008"], []),
             ("Gated work", "working under the gate.", ["POL-0007"], [])]
        )
        errors = ws.validate_errors()
        assert any("POL-0001: principle listed in topic" in e for e in errors)

    def test_anti_pattern_without_co_topic_replacement_fails(self, ws):
        ws.standard_corpus()
        ws.manifest(
            [("Alpha work", "doing alpha things.",
              ["POL-0003", "POL-0004", "POL-0005", "POL-0008"], []),
             ("Gated work", "working under the gate.", ["POL-0007", "POL-0006"], [])]
        )
        errors = ws.validate_errors()
        assert any(
            "POL-0006: no non-principle replacement shares its topic" in e for e in errors
        )

    def test_illegal_axis_value_fails(self, ws):
        ws.standard_corpus()
        errors = ws.validate_errors(compiler="msvc")
        assert any("compiler 'msvc'" in e for e in errors)
