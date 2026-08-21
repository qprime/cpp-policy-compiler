---
id: POL-0203
kind: guideline
trigger: "pass an operation to an algorithm"
attribution:
  - source: standard-practice
    locator: "callables"
    upstream: ["CG T.40"]
---

# Pass an operation to an algorithm as a function object, not a function pointer

Hand over a lambda, a named struct with `operator()`, or a standard functor. Reserve
function pointers for a C boundary.

```cpp
std::ranges::sort(moves, [](const Move& a, const Move& b) {
    return a.start_mm.x < b.start_mm.x;
});

std::sort(moves.begin(), moves.end(), &compare_by_x);   // an indirect call per compare
```

A function object's call operator is known at the instantiation, so the compiler
inlines it. A function pointer is an indirect call the optimizer usually cannot see
through, in the innermost loop of the algorithm.
