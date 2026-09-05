from __future__ import annotations

import json
import shutil
from pathlib import Path

from polc.cli import main
from polc import project

REPOSITORY = Path(__file__).parents[1]
POLICIES = REPOSITORY / "docs/policies"
STANDARD = REPOSITORY / "docs/standard"
EXEMPLARS = REPOSITORY / "docs/exemplars"


def _args(command: str, root: Path, *extra: str) -> list[str]:
    return [
        "project", command, "--root", str(root),
        "--policies", str(POLICIES), "--standard", str(STANDARD),
        "--exemplars", str(EXEMPLARS), *extra,
    ]


def _init(root: Path, adapter: str | None = None) -> None:
    extra = [
        "--name", "managed-test", "--language-version", "20",
        "--compiler", "gcc", "--domain", "application",
    ]
    if adapter:
        extra.extend(("--adapter", adapter))
    assert main(_args("init", root, *extra)) == 0


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*") if path.is_file()
    }


def test_init_is_non_destructive(tmp_path: Path, capsys) -> None:
    root = tmp_path / "target"
    (root / ".polc").mkdir(parents=True)
    authored = root / ".polc/project.md"
    authored.write_text("keep me\n", encoding="utf-8")
    assert main(
        _args(
            "init", root, "--language-version", "20", "--compiler", "gcc",
            "--domain", "application",
        )
    ) == 1
    assert authored.read_text(encoding="utf-8") == "keep me\n"
    assert "refusing to overwrite" in capsys.readouterr().err


def test_build_is_deterministic_and_preserves_inputs(tmp_path: Path) -> None:
    root = tmp_path / "target"
    _init(root)
    context = root / ".polc/context/layers.md"
    context.write_text("# Layers\n\nUI depends on core.\n", encoding="utf-8")
    project_before = (root / ".polc/project.md").read_bytes()
    lock_before = (root / ".polc/lock.json").read_bytes()
    assert main(_args("build", root)) == 0
    first = _snapshot(root)
    assert main(_args("build", root)) == 0
    assert _snapshot(root) == first
    generated_context = root / "policy/generation/layers.md"
    assert generated_context.read_text(encoding="utf-8") == context.read_text(
        encoding="utf-8"
    )
    assert (root / ".polc/project.md").read_bytes() == project_before
    assert (root / ".polc/lock.json").read_bytes() == lock_before


def test_check_detects_hand_edit_without_writing(tmp_path: Path, capsys) -> None:
    root = tmp_path / "target"
    _init(root)
    generated = root / "policy/generation/index.md"
    generated.write_text(generated.read_text(encoding="utf-8") + "hand edit\n", encoding="utf-8")
    before = _snapshot(root)
    assert main(_args("check", root)) == 1
    assert _snapshot(root) == before
    assert "generated output drift" in capsys.readouterr().err
    assert main(_args("build", root)) == 0
    assert "hand edit" not in generated.read_text(encoding="utf-8")


def test_diff_is_read_only_and_accepts_new_corpus(tmp_path: Path, capsys) -> None:
    root = tmp_path / "target"
    _init(root)
    copied = tmp_path / "policies"
    shutil.copytree(POLICIES, copied)
    topic = copied / "TOPICS.md"
    topic.write_text(topic.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    changed_args = _args("diff", root)
    changed_args[changed_args.index(str(POLICIES))] = str(copied)
    before = _snapshot(root)
    assert main(changed_args) == 0
    assert _snapshot(root) == before
    assert "corpus:" in capsys.readouterr().out
    changed_args[1] = "accept"
    assert main(changed_args) == 0
    lock = json.loads((root / ".polc/lock.json").read_text(encoding="utf-8"))
    assert lock["corpus_fingerprint"] != json.loads(before[".polc/lock.json"])["corpus_fingerprint"]


def test_failed_accept_leaves_old_state(tmp_path: Path) -> None:
    root = tmp_path / "target"
    _init(root)
    copied = tmp_path / "policies"
    shutil.copytree(POLICIES, copied)
    policy = next(copied.glob("POL-*.md"))
    policy.write_text("not valid frontmatter\n", encoding="utf-8")
    before = _snapshot(root)
    args = _args("accept", root)
    args[args.index(str(POLICIES))] = str(copied)
    assert main(args) == 1
    assert _snapshot(root) == before


def test_unowned_destination_is_refused(tmp_path: Path, capsys) -> None:
    root = tmp_path / "target"
    destination = root / "policy/generation"
    destination.mkdir(parents=True)
    (destination / "mine.txt").write_text("keep\n", encoding="utf-8")
    assert main(
        _args(
            "init", root, "--language-version", "20", "--compiler", "gcc",
            "--domain", "application",
        )
    ) == 1
    assert (destination / "mine.txt").read_text(encoding="utf-8") == "keep\n"
    assert "unowned" in capsys.readouterr().err


def test_claude_adapter_emits_independent_skills(tmp_path: Path) -> None:
    root = tmp_path / "target"
    _init(root, "claude-code")
    generation = root / ".claude/skills/cpp-policy-generation/SKILL.md"
    review = root / ".claude/skills/cpp-policy-review/SKILL.md"
    assert "name: managed-test-generation" in generation.read_text(encoding="utf-8")
    assert "name: managed-test-review" in review.read_text(encoding="utf-8")
    assert not (root / "CLAUDE.md").exists()


def test_accept_switches_only_owned_adapter_destinations(tmp_path: Path) -> None:
    root = tmp_path / "target"
    _init(root)
    unrelated = root / ".claude/keep.txt"
    unrelated.parent.mkdir()
    unrelated.write_text("keep\n", encoding="utf-8")
    assert main(_args("accept", root, "--adapter", "claude-code")) == 0
    assert not (root / "policy/generation").exists()
    assert not (root / "policy/review").exists()
    assert (root / ".claude/skills/cpp-policy-generation/SKILL.md").is_file()
    assert (root / ".claude/skills/cpp-policy-review/SKILL.md").is_file()
    assert unrelated.read_text(encoding="utf-8") == "keep\n"


def test_interrupted_install_rolls_back_all_outputs(
    tmp_path: Path, monkeypatch
) -> None:
    root = tmp_path / "target"
    _init(root)
    before = _snapshot(root)
    original = Path.replace
    calls = 0

    def fail_once(path: Path, target: Path) -> Path:
        nonlocal calls
        calls += 1
        if calls == 4:
            raise OSError("simulated interruption")
        return original(path, target)

    monkeypatch.setattr(Path, "replace", fail_once)
    inputs = project.Inputs(root, POLICIES, STANDARD, EXEMPLARS)
    try:
        project.accept(inputs)
    except project.PolcError as exc:
        assert "rolled back" in exc.errors[0]
    else:
        raise AssertionError("the simulated interruption did not occur")
    assert _snapshot(root) == before
