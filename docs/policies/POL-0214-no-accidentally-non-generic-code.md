---
id: POL-0214
kind: guideline
trigger: "write a template used with one type"
attribution:
  - source: standard-practice
    locator: "genericity"
    upstream: ["CG T.143"]
---

# A template that only works for one type is not a template

Instantiate a template with at least two types before believing it is generic. Where
the body names a concrete type, uses a member only one type has, or assumes a
specific container, either constrain it or make it concrete.

```cpp
template <class Container>
double total_length_mm(const Container& moves) {
    double total = 0.0;
    for (const Move& move : moves) { total += length_mm(move); }   // Move: not generic
    return total;
}
```

That template compiles only for containers of `Move` and reports it as a body error
in the caller's file. Either the element type is a parameter or the function should
take `std::span<const Move>` and say so.
