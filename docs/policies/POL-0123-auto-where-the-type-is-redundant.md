---
id: POL-0123
kind: standard
attribution:
  - source: testimony/coding-rules-2026-07.md
    locator: "auto #1"
    upstream: ["CG ES.11", "CG T.12"]
---

# `auto` where the type is already on the line or unspellable; the spelled type otherwise

Write `auto` for iterators, `make_*` results, lambdas, and range-`for` bindings.
Spell the type where it is the fact the reader came for. Use `auto` to own and
`const auto&` to read; reserve `auto&&` for range-`for` and generic forwarding.

```cpp
auto it = moves.begin();
auto post = std::make_unique<GrblPost>(dialect);
for (const auto& move : moves) { ... }

const Bounds bounds = bounds_of(polygon);      // the type is the point
auto bounds = bounds_of(polygon);              // tells the reader nothing
```

`auto` earns its place against redundancy — repeating a type the line already names
— not against naming types. Where the right-hand side is a function call, the type
is the one thing the line does not otherwise say.
