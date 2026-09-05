---
id: POL-0014
kind: standard
trigger: "write a function that reaches for global state"
review_trigger: "a function reads state its parameters and object do not name"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #6"
    upstream: ["CG I.1"]
---

# An interface states its whole dependency in its signature

Everything a function needs arrives through its parameters or its object. No
reaching for global state, no ambient configuration, no implicit conversion
deciding which overload runs.

```cpp
Paths plan_pocket(const PlanarFace& face, const Tool& tool,
                  const PocketParams& params);

Paths plan_pocket(const PlanarFace& face);   // reads g_active_tool, g_settings
```

The second signature cannot be called twice with different tools, cannot be
tested without building the world, and cannot be read without searching the
translation unit for what else it touches.
