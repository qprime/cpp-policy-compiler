"""Compare two independently built wheels and their installed stock archives."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import venv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    output = args.out.resolve()
    if output.exists():
        parser.error("--out must name a new directory for clean builds")
    output.mkdir(parents=True)
    repository = Path(__file__).resolve().parents[1]
    results: list[dict[str, str]] = []
    for name in ("first", "second"):
        root = output / name
        root.mkdir()
        wheels = root / "wheels"
        subprocess.run(
            [sys.executable, "-m", "build", "--wheel", "--no-isolation",
             "--outdir", str(wheels)], cwd=repository, check=True,
        )
        wheel, = wheels.glob("*.whl")
        environment = root / "environment"
        venv.EnvBuilder(with_pip=True, system_site_packages=True).create(environment)
        python = environment / "bin/python"
        subprocess.run(
            [str(python), "-m", "pip", "install", "--no-deps", "--force-reinstall",
             str(wheel)], check=True,
        )
        archives = root / "archives"
        subprocess.run(
            [str(python), "-m", "polc.cli", "release", "build", "--out", str(archives)],
            cwd=root, check=True,
        )
        artifacts = [wheel, *sorted(archives.glob("*.zip"))]
        if len(artifacts) != 3:
            raise RuntimeError("expected one wheel and two stock archives")
        results.append({
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in artifacts
        })
    if results[0] != results[1]:
        raise RuntimeError(f"release builds differ: {results}")
    for name, digest in sorted(results[0].items()):
        print(f"{digest}  {name}")


if __name__ == "__main__":
    main()
