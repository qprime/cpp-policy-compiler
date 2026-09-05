---
id: POL-0229
kind: standard
trigger: "represent a quantity that has a unit"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: when a thing becomes a type"
    upstream: ["CG I.4"]
---

# A dimensioned scalar uses the lightest representation that prevents unit confusion

Use a unit-suffixed primitive when local arithmetic is clear and interfaces cannot
transpose like-typed quantities. Introduce a strong type when unit confusion or
parameter transposition is a material interface risk. If arithmetic must preserve
units, use a coherent units abstraction rather than a partial wrapper that callers
repeatedly unwrap.

```cpp
const double r_eff_mm = std::max(0.01, (bore_d_mm - tool_d_mm) * 0.5);       // clear

const Millimeters r_eff = std::max(Millimeters{0.01},
                                   (bore_d - tool_d) * Millimeters{0.5});   // worse
```

A type that supports the full arithmetic of geometry correctly *is* a units
library — real infrastructure with real cost. A partial one produces ceremony
without safety: every expression grows constructor calls, and the one operation
you forgot to define sends the author back to the primitive anyway.

Unit suffixes plus params structs often close the transposition hole at lower cost.
They are naming conventions, however, not type-system enforcement; choose the
stronger representation when an invalid unit combination should be ill-formed.
