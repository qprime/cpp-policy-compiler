---
id: POL-0229
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: when a thing becomes a type"
    upstream: ["CG I.4"]
---

# A dimensioned scalar stays a primitive with a unit-suffixed name

Introduce a strong typedef only when both hold: two units of the same underlying
type are genuinely confusable at a boundary, **and** arithmetic does not flow
through the type. One without the other is not enough.

```cpp
const double r_eff_mm = std::max(0.01, (bore_d_mm - tool_d_mm) * 0.5);       // clear

const Millimeters r_eff = std::max(Millimeters{0.01},
                                   (bore_d - tool_d) * Millimeters{0.5});   // worse
```

A type that supports the full arithmetic of geometry correctly *is* a units
library — real infrastructure with real cost. A partial one produces ceremony
without safety: every expression grows constructor calls, and the one operation
you forgot to define sends the author back to the primitive anyway.

Unit suffixes plus params structs already close the transposition hole that
motivates wrapping, at a fraction of the cost. Reach for a strong typedef at a
confusable boundary where the value is *carried*, not computed.
