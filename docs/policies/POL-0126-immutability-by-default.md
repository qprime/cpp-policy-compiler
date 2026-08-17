---
id: POL-0126
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: immutability by default"
    upstream: ["CG P.10", "CG Con.1", "CG Con.4", "CG ES.25"]
---

# Write `const` first and remove it when you need to mutate

Every local, member, parameter, and namespace-scope value starts `const` or
`constexpr`. Drop it only when the code actually assigns.

```cpp
const Bounds b = bounds_of(polygon);
constexpr double kMinMarginMm = 10.0;

double total_mm = 0.0;                 // non-const: it accumulates, and says so
for (const Move& move : moves) { total_mm += length_mm(move); }
```

A non-`const` local in the middle of a function is a signal to the reader that it
changes; if it does not change, the signal is a lie and they check anyway.
Immutable data also cannot be corrupted by a caller nobody thought about.

`mutable` members exist for caches and are otherwise a smell.
