---
id: STD-0017
group: layout-of-the-line
enforced_by: clang-tidy
attribution:
  - source: standard-practice
    locator: "declaration and statement layout"
    upstream: ["CG NL.20", "CG NL.21", "CG ES.10"]
---

# One statement per line, one name per declaration

```cpp
const double step_over_mm = 6.0;
const double step_down_mm = 2.0;

double step_over_mm = 6.0, step_down_mm = 2.0;      // no
if (face.empty()) { return {}; } else { plan(); }   // no
```

A declaration per line is what makes `int* a` mean what it looks like, keeps a
diff to the line that changed, and gives a debugger one place to break.
