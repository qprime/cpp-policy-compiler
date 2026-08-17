---
id: POL-0033
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: named operation"
    upstream: ["CG F.8"]
---

# Prefer a function whose result depends only on its arguments

Take the inputs, return the output, touch nothing else. Where state must change,
confine the mutation to one function and keep the computation pure.

```cpp
Paths plan_pocket(const PlanarFace& face, const PocketParams& params);   // pure

void plan_pocket(const PlanarFace& face);   // appends to a member, logs, caches
```

A pure function is testable with one call and readable without context. Its
result also cannot depend on what ran before it, which is what makes a defect in
it reproducible.
