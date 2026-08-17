---
id: POL-0069
kind: guideline
attribution:
  - source: standard-practice
    locator: "regular types"
    upstream: ["CG C.11"]
---

# A concrete value type behaves like `int`

Give it copy, move, equality, and a default constructor if a default value makes
sense; let the compiler write all of them where it can. Then it works in
containers, algorithms, and tests without special handling.

```cpp
struct Vec2 {
    double x = 0.0;
    double y = 0.0;
    friend bool operator==(const Vec2&, const Vec2&) = default;
};
```

Regularity is what lets a type be used without reading it. A value type missing
equality cannot be compared in a test; missing copy, it cannot be stored in a
`std::vector`; and each gap forces callers into workarounds that outlive the
reason for them.
