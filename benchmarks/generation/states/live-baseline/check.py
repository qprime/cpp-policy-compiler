from pathlib import Path

source = Path("sample.cpp").read_text(encoding="utf-8")
raise SystemExit("make_result" not in source or "find_value" not in source)
