---
id: POL-0104
kind: standard
attribution:
  - source: standard-practice
    locator: "preprocessor use"
    upstream: ["CG Enum.1", "CG ES.30", "CG ES.31"]
---

# No macros for constants, functions, or program text

A constant is `constexpr`. A function is a function, or a `constexpr` function. A
repeated declaration is a template. The remaining legitimate macros are include
guards and conditional compilation on a platform.

```cpp
constexpr double kMinMarginMm = 10.0;
constexpr double radius_mm(double diameter_mm) { return 0.5 * diameter_mm; }

#define MIN_MARGIN_MM 10.0                              // no type, no scope
#define RADIUS_MM(d) (0.5 * (d))                        // no type, no overloading
```

A macro is text substitution running before the language exists: it ignores scope,
namespaces, and types, it cannot be inspected in a debugger, and its errors are
reported at the expansion site with the definition nowhere in view.
