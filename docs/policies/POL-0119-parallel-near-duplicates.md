---
id: POL-0119
kind: anti-pattern
trigger: "write a function that shares most of its body with another"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: parallel near-duplicates"
    upstream: ["CG ES.3"]
replacement: ["POL-0118"]
---

# Two functions sharing most of their bodies

```cpp
Paths plan_pocket_raster(const PlanarFace& face, double step_over_mm) {
    auto rings = build_inset_rings(face, step_over_mm);
    // 40 shared lines
    return emit_raster(rings);
}

Paths plan_pocket_spiral(const PlanarFace& face, double step_over_mm) {
    auto rings = build_inset_rings(face, step_over_mm);
    // the same 40 lines, already one bug fix behind
    return emit_spiral(rings);
}
```

A fix applied to one is forgotten in the other, and the divergence is invisible
because both files still compile and both tests still pass.
