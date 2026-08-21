---
id: POL-0098
kind: standard
trigger: "cast a base reference down to a derived type"
attribution:
  - source: standard-practice
    locator: "hierarchy navigation"
    upstream: ["CG C.146", "CG C.147", "CG C.148", "CG C.153"]
---

# Prefer a virtual function to a cast; where navigation is unavoidable, `dynamic_cast`

Add the operation to the interface. Where the hierarchy genuinely must be
navigated, `dynamic_cast` to a reference when failure is a bug, and to a pointer
when failure is an expected alternative.

```cpp
auto& grbl = dynamic_cast<GrblPost&>(post);     // failure is a bug: throws
if (auto* grbl = dynamic_cast<GrblPost*>(&post)) {   // failure is expected
    ...
}
```

`static_cast` down a hierarchy is undefined behaviour when the object is not what
you assumed, and it compiles. `dynamic_cast` is checked, and choosing the
reference or pointer form is how you say whether a miss is an error or a branch.

A chain of `dynamic_cast` tests over sibling types is a virtual function that was
never written.
