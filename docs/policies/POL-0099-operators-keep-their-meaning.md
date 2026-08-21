---
id: POL-0099
kind: standard
trigger: "overload an operator"
attribution:
  - source: standard-practice
    locator: "operator overloading"
    upstream: ["CG C.160", "CG C.162", "CG C.163", "CG C.167"]
---

# An operator keeps its conventional meaning, or it is a named function

Overload an operator only where the operation is what the symbol already means to
every C++ reader: `+` composes, `==` compares, `[]` indexes, `<<` inserts into a
stream. Overload the whole family of roughly equivalent operations, and nothing
beyond it.

```cpp
Vec2 operator+(Vec2 a, Vec2 b);          // conventional
Vec2& operator+=(Vec2& a, Vec2 b);       // same family: provide it too

Paths operator+(const Job& job, const Tool& tool);   // no — this is plan_pocket
```

An operator with a private meaning is a function whose name the reader cannot
look up and whose precedence they did not choose. Providing `+` without `+=`
leaves callers writing `a = a + b` where every other type in the language accepts
the compound form.
