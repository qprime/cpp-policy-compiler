---
id: POL-0200
kind: standard
trigger: "write a concept"
attribution:
  - source: standard-practice
    locator: "concept design"
    upstream: ["CG T.20", "CG T.21", "CG T.22", "CG T.23", "CG T.26", "CG T.41"]
---

# A concept names a semantic requirement with a complete set of operations

Define a concept around what the type must *mean*, list every operation the template
actually uses, and require nothing beyond that. Refine a concept by adding use
patterns, not by restating syntax. Where the semantics cannot be checked, say them in
a comment beside the concept.

```cpp
template <class T>
concept Offsettable = requires(const T& shape, double delta_mm) {
    { offset(shape, delta_mm) } -> std::same_as<T>;
    { area_mm2(shape) } -> std::convertible_to<double>;
};
// Semantics: offset(s, d) has area >= area(s) for d >= 0, and offset(s, 0) == s.
```

A concept requiring only `T::value_type` exists is a syntax filter: two unrelated
types satisfy it and the template compiles for both, so the constraint reports
nothing useful. An incomplete set is worse than none, because the template compiles
for a type it will fail on later, at a different call site.

Requiring properties the template does not use rejects types that would have worked.
