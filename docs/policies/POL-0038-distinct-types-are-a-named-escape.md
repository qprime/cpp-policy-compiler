---
id: POL-0038
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 3: dimensioned scalars stay primitives"
  - source: cpp-convention/conventions.md
    locator: "Decision: when a thing becomes a type, on strong typedefs"
---

# A distinct type for a dimensioned scalar is a named escape, not the default

A dimensioned value is a primitive with a unit-suffixed name (POL-0017). Wrapping
it in a distinct type is permitted under two conditions, both required:

- two units of the same underlying type are genuinely confusable at a boundary,
  **and**
- arithmetic does not flow through the type.

Where the value is carried rather than computed, the wrapper costs one
conversion at each end and removes a class of transposition. Where the value is
computed, it costs an operator for every arithmetic form the code uses.

```cpp
const double budget_ms = std::max(1.0, (deadline_ms - elapsed_ms) * 0.5);      // clear
const Millis budget = std::max(Millis{1.0}, (deadline - elapsed) * Millis{0.5});  // worse
```

A type that supports the full arithmetic of a domain correctly is a units
library, which is real infrastructure with real cost. A partial one produces
ceremony without safety: every operation it does not define is an operation the
author writes around, usually by unwrapping, which is where the safety went.

Unit suffixes plus params structs (POL-0023) already close the transposition
hole that motivates wrapping, at a fraction of the cost. The escape exists for
the case they do not cover, which is a boundary that hands over a bare scalar.
