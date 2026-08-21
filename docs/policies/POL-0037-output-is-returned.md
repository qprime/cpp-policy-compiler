---
id: POL-0037
kind: standard
trigger: "return more than one value, or write an out parameter"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: how to pass a parameter"
    upstream: ["CG F.20", "CG F.21"]
---

# Output comes back as a return value, and several outputs come back as a struct

Return the result. Where there are two or more results, return a named struct —
never an out-parameter, and never a `std::pair` whose members are called `first`
and `second`.

```cpp
struct PocketPlan {
    Paths paths;
    double actual_step_over_mm;
    int ring_count;
};

PocketPlan plan_pocket(const PlanarFace& face, const PocketParams& params);

void plan_pocket(const PlanarFace& face, const PocketParams& params,
                 Paths* out_paths, double* out_step_over_mm, int* out_rings);
```

An out-parameter forces the caller to declare an uninitialized object, hides
whether the callee writes it on failure, and cannot be used in an expression.
The named struct also documents the result at the definition rather than at every
call.
