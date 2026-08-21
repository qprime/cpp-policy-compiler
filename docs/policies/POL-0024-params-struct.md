---
id: POL-0024
kind: pattern
trigger: "pass more than four parameters, or two adjacent of the same type"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: params struct"
    upstream: ["CG I.23", "CG I.24"]
---

# Parameters that can be transposed become a named struct

Two triggers, either one sufficient: more than four parameters, or two adjacent
parameters of the same type. Move them into a struct and call with designated
initializers.

```cpp
Paths plan_pocket(const PlanarFace& face, const Tool& tool, double step_over_mm,
                  double step_down_mm, double safe_z_mm, double ramp_angle_deg);

plan_pocket(face, tool, 6.0, 2.0, 5.0, 30.0);
//                      ^^^^^^^^^^^^^^^^^^^ transpose any pair; still compiles
```

```cpp
struct PocketParams {
    double step_over_mm;
    double step_down_mm;
    double safe_z_mm;
    double ramp_angle_deg;
    PocketStrategy strategy = PocketStrategy::Raster;
};

Paths plan_pocket(const PlanarFace& face, const Tool& tool,
                  const PocketParams& params);

plan_pocket(face, tool, PocketParams{
    .step_over_mm = 6.0,
    .step_down_mm = 2.0,
    .safe_z_mm = 5.0,
    .ramp_angle_deg = 30.0,
});
```

The defect is not the count, it is that the compiler cannot tell a correct call
from a transposed one. Distinct types close the same hole by making the
transposition ill-formed; either route satisfies this, and you are not required
to do both.

Escape: genuinely ordered mathematical arguments where the order *is* the
convention — `lerp(a, b, t)`, `clamp(v, lo, hi)`, `atan2(y, x)`.
