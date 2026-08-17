---
id: POL-0030
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "6. Immutability"
    upstream: ["CG F.4", "CG Con.5", "CG T.123"]
---

# A value or function computable at compile time is `constexpr`

Write `constexpr` on every namespace-scope constant and on any function whose
arguments could be constants. Reach for `consteval` only where compile-time
evaluation is required rather than possible.

```cpp
constexpr double kMinMarginMm = 10.0;
constexpr double radius_mm(double diameter_mm) { return 0.5 * diameter_mm; }

constexpr double kSafeZMm = radius_mm(12.0) + kMinMarginMm;   // no run-time work
```

A `constexpr` function still works at run time, so the annotation costs nothing
and moves what it can to the compiler. It also makes the value usable where a
constant expression is required, which a `const` double is not.
