---
id: POL-0001
kind: principle
precedence: 1
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #1"
    upstream: ["CG P.4", "CG P.5"]
---

# Correct by construction beats correct by test

Take the earliest of these that closes the defect:

1. Make the wrong program ill-formed — distinct types, `enum class`, exhaustive
   dispatch.
2. Make the wrong object unconstructible — a constructor that rejects the input.
3. Check once at a boundary and encode the result in a type.
4. Test the resulting behavior and the boundaries that establish the invariant.

```cpp
enum class Units { Millimeters, Inches };
double to_mm(double value, Units units);      // a transposed call will not compile
double to_mm(double value, bool is_metric);   // a transposed call compiles
```

A passing test samples behavior; a type can make a whole class of invalid
programs or states unrepresentable. Tests still verify that the chosen types and
boundary checks implement the required behavior. Do not use a test as the only
home for an invariant that the program can enforce structurally.
