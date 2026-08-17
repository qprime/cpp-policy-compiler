---
id: POL-0134
kind: anti-pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: magic number"
    upstream: ["CG ES.45"]
replacement: ["POL-0133"]
---

# An inline numeric literal in a check or a computation

```cpp
if (margin_mm < 10.0) { ... }                    // 10.0 what? decided by whom?
const double feed = rpm * 0.002 * 4;             // three unnamed facts
```

The value has no searchable identity, so the next site that needs the same limit
gets its own literal, and the two diverge the first time one is tuned. Nothing
records what the number meant or who chose it.
