---
id: POL-0005
kind: principle
precedence: 5
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #5"
    upstream: ["CG P.7"]
---

# Defensive at boundaries, trusting inside

Validate where untrusted data enters — user input, file parsing, FFI. Past that
line, trust it.

```cpp
// boundary: the only place a bad value can be rejected
ToolTable load_tool_table(const std::filesystem::path& path);  // throws on bad input

// internal: no re-check, the type already carries the guarantee
double chip_load_mm(const Tool& tool, double feed_mm_per_min);
```

Defensive checks scattered through internals are a symptom of an invariant that
was never established. Each copy of the check is a place the fallback can differ
from its siblings.
