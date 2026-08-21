---
id: POL-0141
kind: standard
trigger: "compare two pointers"
attribution:
  - source: standard-practice
    locator: "pointer comparison"
    upstream: ["CG ES.62"]
---

# Only compare pointers into the same object or array

Compare iterators from the same container, or pointers into the same array. Use
equality against `nullptr` freely; relational comparison needs a common object.

```cpp
if (it != moves.end()) { ... }                 // same container

if (&lhs_moves[0] < &rhs_moves[0]) { ... }     // unrelated arrays: unspecified
```

Relational comparison between pointers into different objects is unspecified, so
the result can differ between builds and can be inconsistent within one run. Where
you need a stable order over unrelated objects, order them by something they own.
