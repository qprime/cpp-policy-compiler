---
id: POL-0052
kind: guideline
trigger: "add an overload that only fills in an argument"
attribution:
  - source: standard-practice
    locator: "default arguments"
    upstream: ["CG F.51"]
---

# Prefer a default argument to an overload that only fills one in

When overloads differ only in how many trailing arguments they take, write one
function with defaults. Keep separate overloads when the bodies genuinely differ.

```cpp
Paths plan_pocket(const PlanarFace& face, double step_over_mm,
                  PocketStrategy strategy = PocketStrategy::Raster);

Paths plan_pocket(const PlanarFace& face, double step_over_mm);
Paths plan_pocket(const PlanarFace& face, double step_over_mm,
                  PocketStrategy strategy);         // forwards to the other
```

The forwarding overload is a second declaration to keep in step, a second entry
in every reader's overload resolution, and a place for the two bodies to drift.
The default argument states the same fact once.
