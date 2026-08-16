from polc.cli import main


class TestCli:
    def test_build_writes_the_projection(self, ws):
        ws.standard_corpus()
        config_path = ws.config()
        out = ws.root / "out"
        rc = main(
            ["build", "--config", str(config_path), "--policies", str(ws.policies),
             "--out", str(out)]
        )
        assert rc == 0
        assert (out / "index.md").exists()

    def test_build_reports_document_sizes(self, ws, capsys):
        ws.standard_corpus()
        projection, _, _ = ws.project()
        config_path = ws.config()
        rc = main(
            ["build", "--config", str(config_path), "--policies", str(ws.policies),
             "--out", str(ws.root / "out")]
        )
        assert rc == 0
        out = capsys.readouterr().out
        assert f"index.md: {len(projection.entry)} chars" in out
        assert f"alpha-work.md: {len(projection.topic_documents['alpha-work'])} chars" in out

    def test_failure_never_writes_partial_output(self, ws):
        ws.standard_corpus()
        config_path = ws.config(compiler="msvc")
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
