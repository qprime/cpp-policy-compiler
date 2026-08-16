---
id: POL-0103
kind: standard
attribution:
  - source: standard-practice
    locator: "enumerations"
    upstream: ["CG Enum.1", "CG Enum.3"]
---

# Every enumeration is an `enum class`

```cpp
// Never. Converts to int, so it compares equal to an unrelated enumeration.
enum CompactMode { Full, Incremental };

// Right.
enum class CompactMode { Full, Incremental };
```

An unscoped `enum` is permitted only to match a C API, for the reason POL-0046
permits a pointer-and-length pair at the same boundary: the foreign declaration
dictates the shape.

A macro or an integer constant where an enumeration belongs is the same defect
with less syntax. Both give up the distinct type, and with it the exhaustive
dispatch POL-0033 depends on.

An unscoped enumerator converts implicitly to `int`, so it can be passed where
a number is expected, compared against a different enumeration, and used in
arithmetic, all without a diagnostic. The enumeration then documents a closed
set that the type system is not enforcing, which is the gap POL-0043 names for
strings. `enum class` makes the set closed in the compiler rather than in the
reader's memory (POL-0008).
