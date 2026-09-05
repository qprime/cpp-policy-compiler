from __future__ import annotations

import json
import subprocess
import sys
import venv
import zipfile
from pathlib import Path

import pytest

from polc.cli import main
from polc.corpus import fingerprint

REPOSITORY = Path(__file__).parents[1]
POLICIES = REPOSITORY / "docs/policies"
STANDARD = REPOSITORY / "docs/standard"
EXEMPLARS = REPOSITORY / "docs/exemplars"


@pytest.fixture(scope="module")
def installed(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    root = tmp_path_factory.mktemp("installed-distribution")
    wheel_directory = root / "wheel"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--wheel",
            "--no-isolation",
            "--outdir",
            str(wheel_directory),
        ],
        cwd=REPOSITORY,
        check=True,
    )
    wheel = next(wheel_directory.glob("polc-*.whl"))
    environment = root / "environment"
    venv.EnvBuilder(with_pip=True, system_site_packages=True).create(environment)
    python = environment / "bin/python"
    subprocess.run(
        [python, "-m", "pip", "install", "--no-deps", str(wheel)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    return wheel, python


def test_wheel_contains_complete_canonical_corpus(
    installed: tuple[Path, Path],
) -> None:
    wheel, _ = installed
    expected = {
        f"polc/data/{root.name}/{path.relative_to(root).as_posix()}"
        for root in (POLICIES, STANDARD, EXEMPLARS, REPOSITORY / "docs/configurations")
        for path in root.rglob("*")
        if path.is_file()
    }
    with zipfile.ZipFile(wheel) as archive:
        assert expected <= set(archive.namelist())


def test_installed_cli_builds_without_checkout_and_is_reproducible(
    installed: tuple[Path, Path], tmp_path: Path
) -> None:
    _, python = installed
    executable = python.parent / "polc"
    project = tmp_path / "project"
    command = [
        executable,
        "project",
        "init",
        "--root",
        project,
        "--language-version",
        "20",
        "--compiler",
        "gcc",
        "--domain",
        "application",
    ]
    subprocess.run(command, cwd=tmp_path, check=True)
    subprocess.run(
        [executable, "project", "check", "--root", project],
        cwd=tmp_path,
        check=True,
    )
    before = {
        path.relative_to(project): path.read_bytes()
        for path in project.rglob("*")
        if path.is_file()
    }
    subprocess.run(
        [executable, "project", "build", "--root", project],
        cwd=tmp_path,
        check=True,
    )
    after = {
        path.relative_to(project): path.read_bytes()
        for path in project.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_installed_fingerprint_and_archives_match_repository(
    installed: tuple[Path, Path], tmp_path: Path
) -> None:
    _, python = installed
    script = (
        "from polc.corpus import fingerprint; "
        "from polc.resources import installed_corpus; "
        "p=installed_corpus(); print(fingerprint(p.policies,p.standard,p.exemplars))"
    )
    installed_fingerprint = subprocess.check_output(
        [python, "-c", script], cwd=tmp_path, text=True
    ).strip()
    assert installed_fingerprint == fingerprint(POLICIES, STANDARD, EXEMPLARS)
    executable = python.parent / "polc"
    first, second = tmp_path / "first", tmp_path / "second"
    subprocess.run([executable, "release", "build", "--out", first], check=True)
    subprocess.run([executable, "release", "build", "--out", second], check=True)
    assert {path.name: path.read_bytes() for path in first.glob("*.zip")} == {
        path.name: path.read_bytes() for path in second.glob("*.zip")
    }
    for archive in first.glob("*.zip"):
        subprocess.run([executable, "release", "verify", archive], check=True)
        with zipfile.ZipFile(archive) as source:
            manifest = json.loads(source.read("manifest.json"))
            assert manifest["corpus_fingerprint"] == installed_fingerprint
            assert manifest["projection_format_version"] == 1


def test_projection_format_mismatch_is_explicit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "project"
    corpus = [
        "--policies", str(POLICIES), "--standard", str(STANDARD),
        "--exemplars", str(EXEMPLARS),
    ]
    assert main(
        [
            "project", "init", "--root", str(root), *corpus,
            "--language-version", "20", "--compiler", "gcc",
            "--domain", "application",
        ]
    ) == 0
    lock_path = root / ".polc/lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["projection_format_version"] = 999
    lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    before = {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }
    assert main(["project", "check", "--root", str(root), *corpus]) == 1
    assert "projection format 999" in capsys.readouterr().err
    assert {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    } == before
    assert main(["project", "diff", "--root", str(root), *corpus]) == 0
    assert {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    } == before
    assert main(["project", "accept", "--root", str(root), *corpus]) == 0
    accepted = json.loads(lock_path.read_text(encoding="utf-8"))
    assert accepted["projection_format_version"] == 1


def test_version_one_lock_can_be_previewed_and_migrated(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "project"
    corpus = [
        "--policies", str(POLICIES), "--standard", str(STANDARD),
        "--exemplars", str(EXEMPLARS),
    ]
    assert main(
        [
            "project", "init", "--root", str(root), *corpus,
            "--language-version", "20", "--compiler", "gcc",
            "--domain", "application",
        ]
    ) == 0
    lock_path = root / ".polc/lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["version"] = 1
    del lock["projection_format_version"]
    lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    assert main(["project", "check", "--root", str(root), *corpus]) == 1
    assert "lock schema 1" in capsys.readouterr().err
    assert main(["project", "diff", "--root", str(root), *corpus]) == 0
    assert main(["project", "accept", "--root", str(root), *corpus]) == 0
    migrated = json.loads(lock_path.read_text(encoding="utf-8"))
    assert migrated["version"] == 2
    assert migrated["projection_format_version"] == 1
