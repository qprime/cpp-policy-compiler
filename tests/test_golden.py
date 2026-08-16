from pathlib import Path

from polc.cli import main

REPO = Path(__file__).resolve().parent.parent
GOLDEN = Path(__file__).resolve().parent / "golden" / "cpp20-gcc-application"


class TestGolden:
    def test_full_corpus_projection_matches_golden(self, update_goldens, tmp_path):
        out = tmp_path / "projection"
        rc = main(
            [
                "build",
                "--config",
                str(REPO / "docs" / "configurations" / "cpp20-gcc-application.md"),
                "--policies",
                str(REPO / "docs" / "policies"),
                "--out",
                str(out),
            ]
        )
        assert rc == 0
        built = {p.name: p.read_text(encoding="utf-8") for p in out.iterdir()}

        if update_goldens:
            GOLDEN.mkdir(parents=True, exist_ok=True)
            for stale in GOLDEN.iterdir():
                stale.unlink()
            for name, text in built.items():
                (GOLDEN / name).write_text(text, encoding="utf-8")

        golden = {p.name: p.read_text(encoding="utf-8") for p in GOLDEN.iterdir()}
        assert built == golden
