---
id: STD-0001
group: files-and-layout
enforced_by: review
attribution:
  - source: cpp-convention/conventions.md
    locator: "Divergences: [CG SF.1]"
    upstream: ["CG SF.1", "CG NL.27"]
---

# Headers are `.hpp` and sources are `.cpp`

```
include/proj/algo/plan_2d.hpp
algo/plan_2d.cpp
```

`.h` is reserved for C headers reachable from both languages. The distinction is
visible at a glance in a mixed FFI tree, which `.h` for both would erase.
