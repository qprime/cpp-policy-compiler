---
id: POL-0137
kind: standard
trigger: "write NULL or 0 for a pointer"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "13. Standard-specific bans"
    upstream: ["CG ES.47"]
---

# A null pointer is `nullptr`

Never `0`, never `NULL`.

```cpp
const Tool* tool = nullptr;
if (tool == nullptr) { ... }

const Tool* tool = NULL;      // an integer macro wearing a pointer's name
```

`0` and `NULL` are integers, so they pick the `int` overload where both an `int`
and a pointer overload exist, and they deduce as `int` in a template. `nullptr` has
a pointer type and cannot do either.
