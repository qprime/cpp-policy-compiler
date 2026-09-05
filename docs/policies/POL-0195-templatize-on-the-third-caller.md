---
id: POL-0195
kind: standard
trigger: "write a template"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: premature template"
    upstream: ["CG T.1", "CG T.2", "CG T.3"]
---

# Write the concrete type until a demonstrated generic requirement exists

Reach for a template when the operation is genuinely defined over a family of types
and static polymorphism is part of its contract—for example a container, iterator
algorithm, or constrained customization point. A caller count is evidence to
inspect, not a semantic threshold: three unrelated callers do not create one
abstraction, and two types can already establish a real generic operation.

```cpp
double area_mm2(const ConvexPolygon& poly);       // one shape: concrete

template <class Shape>                            // demonstrated shape abstraction
double area_mm2(const Shape& shape);
```

A template's errors appear at instantiation, in the caller's file, naming types the
author never wrote. That cost is worth paying for real genericity and is pure loss
for a function whose generic requirement is only hypothetical.
