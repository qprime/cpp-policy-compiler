---
id: STD-0021
group: layout-of-the-line
enforced_by: clang-tidy
attribution:
  - source: standard-practice
    locator: "function declarations"
    upstream: ["CG NL.25"]
---

# An empty argument list is `()`

```cpp
double area_mm2();
double area_mm2(void);       // no
```

`(void)` is the C spelling for a prototype that takes nothing. In C++ `()` already
means exactly that, so the extra token carries no information.
