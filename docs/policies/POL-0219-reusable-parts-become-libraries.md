---
id: POL-0219
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Dependency Direction"
    upstream: ["CG A.1", "CG A.2"]
---

# A part with its own reason to exist becomes a library, and stable code does not depend on unstable code

When a group of files has a coherent purpose and no dependency on the application
around it, give it its own target. Keep the dependency direction from unstable toward
stable, never the reverse.

```
geom/        stable: no dependency on anything below
ir/          stable: depends on geom
planner/     changing weekly: depends on ir, geom
cli/         changing daily: depends on planner
```

A separate target is what makes the dependency direction checkable by the build
rather than by review. When stable code depends on unstable code, every change to the
unstable part recompiles and re-tests the stable part, and the stable part cannot be
reused without dragging the unstable one along.
