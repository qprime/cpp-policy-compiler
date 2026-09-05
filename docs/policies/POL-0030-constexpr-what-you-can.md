---
id: POL-0030
kind: standard
trigger: "declare a value or function computable at compile time"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "6. Immutability"
    upstream: ["CG F.4", "CG Con.5", "CG T.123"]
---

# A value or function required in constant expressions is `constexpr`

Write `constexpr` on namespace-scope constants and functions that form part of a
compile-time interface or are usefully evaluated during compilation. Reach for
`consteval` only where compile-time evaluation is required rather than possible.

```cpp
constexpr double kMinMarginMm = 10.0;
constexpr double radius_mm(double diameter_mm) { return 0.5 * diameter_mm; }

constexpr double kSafeZMm = radius_mm(12.0) + kMinMarginMm;   // no run-time work
```

A `constexpr` function can still work at run time, but the annotation constrains
its definition and dependencies. Use it to make an intentional constant-expression
contract available, not merely because a trivial function happens to qualify today.
