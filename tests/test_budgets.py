from polc.cli import main


def _measure(ws):
    projection, _, _ = ws.project()
    return len(projection.entry), max(
        len(text) for text in projection.topic_documents.values()
    )


class TestBudgets:
    def test_exact_budget_passes(self, ws):
        ws.standard_corpus()
        entry_size, topic_max = _measure(ws)
        config_path = ws.config(
            budgets={"entry_chars": entry_size, "topic_chars": topic_max}
        )
        out = ws.root / "out"
        rc = main(
            ["build", "--config", str(config_path), "--policies", str(ws.policies),
             "--out", str(out)]
        )
        assert rc == 0
        assert (out / "index.md").exists()

    def test_overflow_fails_naming_document_size_and_budget(self, ws, capsys):
        ws.standard_corpus()
        entry_size, topic_max = _measure(ws)
        config_path = ws.config(
            budgets={"entry_chars": entry_size - 1, "topic_chars": topic_max}
        )
        rc = main(
            ["build", "--config", str(config_path), "--policies", str(ws.policies),
             "--out", str(ws.root / "out")]
        )
        assert rc == 1
        err = capsys.readouterr().err
        assert "index.md" in err
        assert str(entry_size) in err
        assert str(entry_size - 1) in err
        assert "split the topic in TOPICS.md" in err

    def test_overflow_never_writes_partial_output(self, ws):
        ws.standard_corpus()
        entry_size, topic_max = _measure(ws)
        config_path = ws.config(
            budgets={"entry_chars": entry_size, "topic_chars": topic_max - 1}
        )
        out = ws.root / "out"
        rc = main(
            ["build", "--config", str(config_path), "--policies", str(ws.policies),
             "--out", str(out)]
        )
        assert rc == 1
        assert not out.exists()

    def test_check_writes_nothing(self, ws):
        ws.standard_corpus()
        config_path = ws.config()
        before = sorted(p for p in ws.root.rglob("*"))
        rc = main(["check", "--config", str(config_path), "--policies", str(ws.policies)])
        assert rc == 0
        assert sorted(p for p in ws.root.rglob("*")) == before
