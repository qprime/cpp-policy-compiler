---
id: POL-0143
kind: standard
trigger: "write an if/else chain over one value's alternatives"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "2. Closed-set variation"
    upstream: ["CG ES.70"]
---

# Branching on one value's alternatives is a `switch`, not an if/else chain

```cpp
switch (strategy) {
    case PocketStrategy::Raster:      return plan_raster(face, params);
    case PocketStrategy::Spiral:      return plan_spiral(face, params);
    case PocketStrategy::Trochoidal:  return plan_trochoidal(face, params);
}

if (strategy == PocketStrategy::Raster)        { ... }
else if (strategy == PocketStrategy::Spiral)   { ... }   // adding one compiles fine
```

A `switch` with no `default` over an enumeration makes a missing case a warning —
an error under `-Werror=switch` — so adding an enumerator breaks the build at every
site that must handle it. The if/else chain obtains no such guarantee, and it
repeats the subject on every line.
