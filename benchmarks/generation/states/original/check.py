from pathlib import Path

source = Path("sample.cpp").read_text(encoding="utf-8")
raise SystemExit("find_value" not in source)
