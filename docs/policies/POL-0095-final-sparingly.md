---
id: POL-0095
kind: guideline
trigger: "mark a class final"
attribution:
  - source: standard-practice
    locator: "final"
    upstream: ["CG C.139"]
---

# Use `final` on a class only to state a real design closure

Write `final` on a leaf implementation of an interface, where deriving further
would be a mistake. Do not write it on a class merely because nothing derives from
it today.

```cpp
class GrblPost final : public PostProcessor { ... };   // leaf: says so
class Toolpath final { ... };                          // no: closes nothing
```

On a class with no virtual functions `final` buys no devirtualization and blocks
the private-inheritance and test-double techniques a future reader may need. On a
leaf override it documents a closure the design actually made.
