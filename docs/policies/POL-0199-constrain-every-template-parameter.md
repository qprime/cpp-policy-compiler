---
id: POL-0199
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "9. Generic code"
    upstream: ["CG I.9", "CG T.10", "CG T.11", "CG T.13", "CG T.48"]
---

# Every template parameter states its requirement

Write a concept on C++20 and later — the shorthand form where one type has one
constraint. Where the standard has no concepts, write a `static_assert` in the body
saying the same thing. Prefer a standard concept over a hand-written one, and never
reach for `enable_if` SFINAE where concepts exist.

```cpp
template <std::floating_point T>
T area_mm2(const Polygon<T>& poly);

template <class T>
T area_mm2(const Polygon<T>& poly) {
    static_assert(std::is_floating_point<T>::value,
                  "area_mm2: T must be a floating-point type");
    ...
}
```

An unconstrained parameter fails deep inside the instantiation, pointing at a line
the caller did not write. The constraint moves the diagnostic to the call and states
the requirement where a reader looks for it.
