---
id: POL-0195
kind: standard
trigger: "write a template"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: premature template"
    upstream: ["CG T.1", "CG T.2", "CG T.3"]
---

# Write the concrete type; templatize when a third concrete caller forces it

Two callers are two callers. Reach for a template when a third arrives, when the
alternative is a runtime-typed interface that loses checking, or when the thing being
written is genuinely a container or an algorithm over element types.

```cpp
double area_mm2(const ConvexPolygon& poly);       // one shape: concrete

template <class Shape>                            // three callers, real variation
double area_mm2(const Shape& shape);
```

A template's errors appear at instantiation, in the caller's file, naming types the
author never wrote. That cost is worth paying for real genericity and is pure loss
for a function with one or two call sites.
