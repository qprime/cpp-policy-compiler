---
id: POL-0118
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: parallel near-duplicates"
    upstream: ["CG ES.3"]
---

# Logic that would have to change in two places lives in one

When two functions share more than half their bodies, extract the shared part and
pass the difference — usually as a params struct. The test is whether a future
change would need to be made in both.

```cpp
Paths plan_pocket(const PlanarFace& face, const PocketParams& params);

Paths plan_pocket_raster(const PlanarFace& face, double step_over_mm);
Paths plan_pocket_spiral(const PlanarFace& face, double step_over_mm);   // 80% shared
```

Duplicated logic drifts: the fix goes into the copy the author was looking at.
Accidental similarity that would not co-evolve stays separate — merging those
couples two things that only happen to look alike today.
