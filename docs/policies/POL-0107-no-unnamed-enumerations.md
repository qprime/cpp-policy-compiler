---
id: POL-0107
kind: standard
attribution:
  - source: standard-practice
    locator: "enumeration declarations"
    upstream: ["CG Enum.6"]
---

# An enumeration has a name

Give every enumeration a type name, even when it exists only to hold one constant
— in which case it should be a `constexpr` value instead.

```cpp
enum class ArcDirection { Clockwise, CounterClockwise };

enum { kMaxAxes = 6 };                     // no
constexpr int kMaxAxes = 6;                // instead
```

An unnamed enumeration cannot appear in a signature, so nothing can be typed in
terms of it and every function that takes one of its values takes an `int`. Where
it is being used as a constant, `constexpr` says so with a real type.
