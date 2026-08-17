---
id: POL-0157
kind: guideline
attribution:
  - source: standard-practice
    locator: "designing for optimization"
    upstream: ["CG Per.7", "CG Per.10"]
---

# Leave the optimizer room: concrete types, contiguous data, no hidden indirection

Prefer values to pointers, `std::vector` to node-based containers, and a concrete
type to a virtual call on a hot path. These are design defaults, not
optimizations — they cost nothing to choose up front.

```cpp
std::vector<Move> moves;                          // contiguous, inlinable
std::vector<std::unique_ptr<Move>> moves;         // a pointer chase per element
```

The static type system is what lets the compiler inline, unroll, and keep values in
registers. Each layer of indirection removes information it needs, and unlike a
missing micro-optimization, that is expensive to undo once the design depends on
it.
