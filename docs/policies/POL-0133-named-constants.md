---
id: POL-0133
kind: standard
trigger: "write a literal that carries meaning"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: magic number"
    upstream: ["CG ES.45"]
---

# A literal that carries meaning gets a name

`constexpr` at file scope for a value one module owns; a shared constants header
for a value several modules must agree on.

```cpp
constexpr double kMinMarginMm = 10.0;

if (margin_mm < kMinMarginMm) { ... }
```

Trivially obvious literals — `0`, `1`, `0.5` for a midpoint, array indices — need
no name.

An inline literal in a geometry, timing, or limit check is a value with no
searchable identity, so the second site that needs it gets its own copy and the
two drift. The name is also what makes a change to the value one edit.
