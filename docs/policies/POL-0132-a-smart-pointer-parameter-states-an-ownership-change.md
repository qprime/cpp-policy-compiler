---
id: POL-0132
kind: standard
attribution:
  - source: standard-practice
    locator: "smart pointer parameters"
    upstream: ["CG R.33", "CG R.34", "CG R.35", "CG R.36", "CG R.37"]
---

# A smart pointer parameter appears only where ownership changes

| Parameter | Means |
|-----------|-------|
| `std::unique_ptr<T>` | Takes ownership |
| `std::unique_ptr<T>&` | Reseats the caller's pointer |
| `std::shared_ptr<T>` | Takes a share of ownership |
| `std::shared_ptr<T>&` | May reseat the caller's shared pointer |
| `const std::shared_ptr<T>&` | May retain a share |
| `const T&` or `T*` | Ownership is unchanged — the usual case |

```cpp
// Never. Says "shares ownership", does neither, and costs an atomic increment.
void inspect(std::shared_ptr<const Tool> tool);

// Right.
void inspect(const Tool& tool);
void adopt(std::unique_ptr<Tool> tool);
```

Never pass a pointer or reference obtained by dereferencing an aliased smart
pointer: the callee holds a raw reference whose lifetime depends on a share the
caller may release during the call.

A smart pointer in a signature is a statement about lifetime, which is what
POL-0003 asks every declaration to make answerable. Taking one where ownership
does not change makes that statement falsely, so a reader tracing lifetimes has
to open the body to find that nothing happens. It also constrains every caller
to hold the object that way, which propagates the wrong ownership model outward
from a function that never needed it (POL-0048).
