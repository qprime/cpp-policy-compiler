---
id: POL-0103
kind: guideline
attribution:
  - source: standard-practice
    locator: "generic lambdas"
    upstream: ["CG C.170"]
---

# A lambda that needs to handle several types is a generic lambda

Write one `auto` parameter rather than reaching for a way to overload a closure.
Where the alternatives need genuinely different bodies, write the overload set as
named functions or a visitor.

```cpp
const auto to_mm = [](auto value) { return static_cast<double>(value); };
```

A lambda is one function object with one call operator, so there is no overloading
to do. The generic form gives one body for every type it accepts, which is the
only case where a single closure was the right shape to begin with.
