---
id: POL-0045
kind: standard
trigger: "declare a smart pointer parameter"
attribution:
  - source: standard-practice
    locator: "smart pointer parameters"
    upstream: ["CG F.7", "CG R.30", "CG R.32", "CG R.33", "CG R.34", "CG R.35", "CG R.36"]
---

# A parameter takes a smart pointer only to say something about lifetime

| Parameter | Says |
|-----------|------|
| `std::unique_ptr<T>` by value | the function takes ownership |
| `std::unique_ptr<T>&` | the function may replace what the caller owns |
| `std::shared_ptr<T>` by value | the function keeps a share of ownership |
| `std::shared_ptr<T>&` | the function may reseat the caller's pointer |
| `const T&` or `T*` | the function only looks at it |

```cpp
void adopt(std::unique_ptr<Spindle> spindle);          // ownership moves in
double rpm_of(const Spindle& spindle);                 // just reading
double rpm_of(const std::shared_ptr<Spindle>& s);      // no — refcount for nothing
```

A smart pointer in a signature that says nothing about lifetime narrows the
callable set for no reason: the last line cannot be called with a stack object, a
member, or a `unique_ptr`. Take the reference and the same function serves all
of them.
