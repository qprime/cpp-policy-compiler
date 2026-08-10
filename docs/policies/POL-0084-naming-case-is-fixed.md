---
id: POL-0084
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Naming: case table"
    upstream: ["CG NL.5", "CG NL.8", "CG NL.9", "CG NL.10"]
  - source: cpp-convention/conventions.md
    locator: "Divergences: CG NL.10"
  - source: cpp-convention/conventions.md
    locator: "Divergences: CG SF.1"
enforcement:
  clang_tidy: ["readability-identifier-naming"]
---

# Naming case is fixed, not a per-project choice

| Kind | Case | Example |
|------|------|---------|
| Functions, variables, parameters, members | `snake_case` | `parse_config`, `timeout_ms` |
| Private data members | `snake_case_`, trailing underscore | `max_attempts_` |
| Types: class, struct, enum, alias | `PascalCase` | `RetryPolicy`, `CompactParams` |
| Enumerators | `PascalCase` | `CompactMode::Incremental` |
| Constants at namespace scope | `kPascalCase` | `kMinFillRatio` |
| Macros | `ALL_CAPS`, project-prefixed, and avoid macros | `PROJ_ASSERT` |
| Namespaces | `snake_case`, nested by layer | `proj::store` |
| Files | `snake_case`, `.hpp` and `.cpp` | `compact.cpp` |

`ALL_CAPS` is for macros and nothing else. Type information is not encoded in
names: no Hungarian prefixes, no `_ptr` suffix on a pointer, no `_t` on a type.

`.hpp` rather than `.h` for a C++ header, so a C++ header is distinguishable
from a C header at a glance in a tree that contains both.

The case is fixed rather than recommended because names must cross the FFI seam
unchanged (POL-0057), and unchanged crossing is impossible if each side picks
its own case. That makes this structural rather than cosmetic: a per-project
choice does not merely produce variety, it makes a whole class of rule
unstatable. The upstream guidance offers underscore style as a preference; here
it is a requirement, and the requirement is what the preference cannot supply.
