---
id: POL-0141
kind: standard
trigger: "order two pointers with a relational comparison"
attribution:
  - source: standard-practice
    locator: "pointer comparison"
    upstream: ["CG ES.62"]
---

# Relationally compare pointers only within the same object or array

Compare iterators from the same container, or order pointers within the same
array. Equality and inequality can compare unrelated pointers and `nullptr`;
relational comparison needs a common array object unless an explicit library
ordering such as `std::less` is the intended abstraction.

```cpp
if (it != moves.end()) { ... }                 // same container

if (&lhs_moves[0] < &rhs_moves[0]) { ... }     // unrelated arrays: unspecified
```

Relational comparison between pointers into different objects is unspecified, so
the result can differ between builds and can be inconsistent within one run. Where
you need a stable order over unrelated objects, order them by something they own.
