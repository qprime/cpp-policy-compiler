---
id: POL-0085
kind: standard
attribution:
  - source: standard-practice
    locator: "comparison operators"
    upstream: ["CG C.86", "CG C.87"]
---

# `operator==` is a non-member, symmetric, `noexcept` where it can be, and not on a base

Write it as a hidden friend taking both operands by `const&`. Do not define
equality on a polymorphic base.

```cpp
struct Vec2 {
    double x = 0.0;
    double y = 0.0;
    friend bool operator==(const Vec2&, const Vec2&) = default;
};
```

A member `operator==` converts only its right operand, so `1200.0 == feed`
compiles while `feed == 1200.0` does not, or the reverse. Equality on a base
compares the base parts of two unrelated derived objects and reports them equal,
which is almost never what the caller meant.
