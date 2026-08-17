---
id: POL-0125
kind: standard
attribution:
  - source: standard-practice
    locator: "initialization"
    upstream: ["CG ES.20", "CG ES.23", "CG ES.64", "CG T.68"]
---

# Every object is initialized where it is declared, with braces

Use `{}` for construction and initialization. Fall back to parentheses only where
braces would select an initializer-list constructor you do not want.

```cpp
double margin_mm{0.0};
Vec2 origin{};                                  // both members zero
std::vector<Move> moves{first, second};         // two elements

std::vector<int> counts(4);                     // parentheses: four zeroes
std::vector<int> counts{4};                     // braces: one element, value 4

double margin_mm;                               // no: reads garbage until assigned
```

Reading an uninitialized object is undefined behaviour that usually returns
plausible values, so it survives testing and fails on a different build. Braces
additionally reject narrowing conversions that parentheses accept silently, which
inside a template is the difference between a diagnostic and a truncated value.
