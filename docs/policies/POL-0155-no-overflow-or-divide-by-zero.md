---
id: POL-0155
kind: standard
attribution:
  - source: standard-practice
    locator: "arithmetic ranges"
    upstream: ["CG ES.103", "CG ES.104", "CG ES.105"]
---

# Establish the range before the arithmetic

Check the divisor. Where inputs can reach the type's limits, widen the type, clamp
at the boundary, or check before the operation.

```cpp
if (pass_count <= 0) { return std::nullopt; }
const double step_mm = depth_mm / pass_count;

const double step_mm = depth_mm / pass_count;   // pass_count may be 0
const int total = count_a * count_b;            // may overflow int
```

Signed overflow and integer division by zero are undefined behaviour, so the
compiler is entitled to assume they never happen and optimize on that basis — which
is how the check placed *after* the division gets deleted. Establishing the range
first is the only form that survives optimization.

Build with UBSan in at least one configuration so the cases that slip through are
reported rather than silently miscompiled.
