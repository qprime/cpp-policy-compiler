---
id: POL-0217
kind: standard
trigger: "put a definition in a header"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: module boundary"
    upstream: ["CG SF.2", "CG SF.3"]
---

# A header declares; the source file defines

Anything used by more than one source file is declared in a header. A header carries
no object definitions and no non-`inline` function definitions — only declarations,
type definitions, `constexpr` and `inline` definitions, and templates.

```cpp
// plan_2d.hpp
Paths plan_pocket(const PlanarFace& face, const PocketParams& params);
constexpr double kMinMarginMm = 10.0;

// plan_2d.cpp
Paths plan_pocket(const PlanarFace& face, const PocketParams& params) { ... }
```

A non-`inline` function definition in a header becomes a duplicate symbol as soon as
two source files include it, and an object definition becomes two separate objects
that look like one. Re-declaring a shared function in each source file instead of a
header lets the copies disagree, which the linker will not always catch.
