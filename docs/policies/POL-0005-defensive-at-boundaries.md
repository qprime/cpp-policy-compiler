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

Validate where untrusted data enters — user input, file parsing, FFI — and encode
the validated result so internal code can rely on it. Revalidate when data
crosses another trust boundary or an operation can invalidate the guarantee;
do not repeat the same fallback throughout ordinary internal code.

```cpp
// boundary: the only place a bad value can be rejected
ToolTable load_tool_table(const std::filesystem::path& path);  // throws on bad input

// internal: no re-check, the type already carries the guarantee
double chip_load_mm(const Tool& tool, double feed_mm_per_min);
```

Repeated recovery checks scattered through internals are a symptom of an
invariant that was never established. Internal assertions can still document and
diagnose programmer errors; they are not substitutes for boundary validation.
