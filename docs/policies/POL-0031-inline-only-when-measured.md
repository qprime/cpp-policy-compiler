---
id: POL-0031
kind: guideline
attribution:
  - source: standard-practice
    locator: "inline linkage"
    upstream: ["CG F.5"]
---

# `inline` is for linkage, not for speed

Write `inline` when a function is defined in a header and must not violate the
one-definition rule. Do not write it to make code faster unless a measurement
named that function.

```cpp
// geometry.hpp
inline double radius_mm(double diameter_mm) { return 0.5 * diameter_mm; }
```

The compiler decides inlining from its own cost model and ignores the keyword's
hint in all but pathological cases. Treating `inline` as an optimization request
spreads definitions into headers for nothing and lengthens every build.
