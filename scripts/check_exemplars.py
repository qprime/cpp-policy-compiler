"""Build and execute every canonical exemplar with an installed Catch2 3."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from polc.exemplars import load_exemplars


def _quote(path: Path) -> str:
    return '"' + path.as_posix().replace('"', '\\"').replace(';', '\\;') + '"'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--catch2-prefix", type=Path)
    parser.add_argument("--jobs", type=int, default=2)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    repository = Path(__file__).resolve().parents[1]
    build = args.build_dir.resolve()
    source = build / "source"
    source.mkdir(parents=True, exist_ok=True)
    lines = [
        "cmake_minimum_required(VERSION 3.20)",
        "project(polc_exemplar_checks LANGUAGES C CXX)",
        "find_package(Catch2 3 REQUIRED)",
        "find_package(Threads REQUIRED)",
        "enable_testing()",
    ]
    for exemplar in load_exemplars(repository / "docs/exemplars"):
        root = exemplar.directory.resolve()
        name = exemplar.id.replace("-", "_")
        floor = min(int(value) for value in exemplar.applicability["language_version"])
        sources = sorted(root.rglob("*.cpp"))
        if not any(path.name.endswith("_test.cpp") for path in sources):
            raise ValueError(f"{exemplar.id}: no adjacent tests")
        lines += [
            f"add_executable({name} {' '.join(_quote(path) for path in sources)})",
            f"set_target_properties({name} PROPERTIES CXX_STANDARD {floor} "
            "CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)",
            f"target_include_directories({name} PRIVATE {_quote(root / 'include')} {_quote(root)})",
            f"target_link_libraries({name} PRIVATE Catch2::Catch2WithMain Threads::Threads)",
            f"target_compile_options({name} PRIVATE -Wall -Wextra -Wpedantic "
            "-Wconversion -Wsign-conversion -Werror)",
            f"add_test(NAME {name} COMMAND {name})",
            f"set_tests_properties({name} PROPERTIES WORKING_DIRECTORY {_quote(root)} TIMEOUT 60)",
        ]
    header = repository / "docs/exemplars/EXM-0013-ffi-boundary/include"
    (source / "driver_header.c").write_text(
        '#include "sampler/ffi/driver.h"\nint main(void) { return 0; }\n',
        encoding="utf-8",
    )
    lines += [
        "add_executable(driver_header driver_header.c)",
        f"target_include_directories(driver_header PRIVATE {_quote(header)})",
        "set_target_properties(driver_header PROPERTIES C_STANDARD 11 "
        "C_STANDARD_REQUIRED YES C_EXTENSIONS NO)",
        "target_compile_options(driver_header PRIVATE -Wall -Wextra -Wpedantic -Werror)",
        "add_test(NAME driver_header COMMAND driver_header)",
    ]
    (source / "CMakeLists.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    command = ["cmake", "-S", str(source), "-B", str(build / "build")]
    if args.catch2_prefix:
        command.append(f"-DCMAKE_PREFIX_PATH={args.catch2_prefix.resolve()}")
    subprocess.run(command, check=True)
    subprocess.run(
        ["cmake", "--build", str(build / "build"), "--parallel", str(args.jobs)], check=True
    )
    subprocess.run(
        ["ctest", "--test-dir", str(build / "build"), "--output-on-failure"], check=True
    )


if __name__ == "__main__":
    main()
