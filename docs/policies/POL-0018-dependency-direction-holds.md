---
id: POL-0018
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #8"
  - source: cpp-convention/conventions.md
    locator: "Dependency Direction"
---

# Dependency direction holds

Includes flow one way through the layer stack. A layer may include from layers
downstream of it, never from layers upstream.

```
Input/CLI  →  Parser  →  IR/Model  →  Validation  →  Backend/Output
```

The test for an ambiguous case: delete the higher-level module mentally, and ask
whether the lower-level modules still compile. If they do not, the dependency is
already inverted and the include that inverted it is the defect.

A lower layer that needs a higher layer's type gets an adapter at the boundary
(POL-0087). Pulling the higher layer's headers down is what the rule forbids.

An inverted include is not visible in the file that contains it; it is visible
only in the shape of the whole graph, which no single edit shows. Once the graph
has a cycle, the layers can no longer be built, tested, or reasoned about
separately, and the cost of restoring the direction grows with every edge added
after. The rule is stated as a direction rather than as a set of allowed pairs
so that it holds for layers that do not exist yet.
