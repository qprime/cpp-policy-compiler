---
id: POL-0145
kind: guideline
trigger: "write a default arm"
attribution:
  - source: standard-practice
    locator: "switch default"
    upstream: ["CG ES.79"]
---

# A `default` arm handles a genuinely common case, never a forgotten one

Leave `default` off a `switch` over an enumeration so the compiler reports missing
enumerators. Write it where the subject is an open set — an integer, a parsed
character — or where many alternatives genuinely share one handling.

```cpp
switch (strategy) {                            // no default: exhaustiveness checked
    case PocketStrategy::Raster:      return plan_raster(face, params);
    case PocketStrategy::Spiral:      return plan_spiral(face, params);
    case PocketStrategy::Trochoidal:  return plan_trochoidal(face, params);
}

switch (strategy) {
    case PocketStrategy::Raster: return plan_raster(face, params);
    default: return plan_spiral(face, params);      // silently absorbs new cases
}
```

`default` on a closed set converts the compiler's exhaustiveness report into
silence, which is the one property worth having when an enumerator is added a year
from now.
