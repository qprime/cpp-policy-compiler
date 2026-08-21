---
id: POL-0128
kind: standard
trigger: "declare a sequence of elements"
attribution:
  - source: standard-practice
    locator: "array types"
    upstream: ["CG ES.27", "CG SL.con.1"]
---

# A fixed-size sequence is `std::array`; a growing one is `std::vector`

No C arrays. `std::array<T, N>` when the size is a compile-time constant,
`std::vector<T>` otherwise.

```cpp
std::array<double, 3> offsets_mm{0.0, 0.0, 0.0};
std::vector<Move> moves;

double offsets_mm[3];                            // no
```

A C array decays to a pointer at the first opportunity, losing its size, and it has
no `size()`, no `begin()`, no bounds-checked `at()`, and no value semantics.
`std::array` is the same storage with all of those.

A runtime-sized stack array is a compiler extension; use `std::vector` and let it
allocate.
