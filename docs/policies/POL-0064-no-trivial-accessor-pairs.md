---
id: POL-0064
kind: guideline
trigger: "write a getter and setter around a data member"
attribution:
  - source: standard-practice
    locator: "accessor design"
    upstream: ["CG C.131"]
---

# A getter/setter pair around a bare member means the type has no invariant

When a member can be read and written freely, there is no invariant to protect —
make it an aggregate `struct` with a public member. Keep an accessor when it
computes, validates, or narrows access.

```cpp
struct PocketParams {
    double step_over_mm;           // no invariant: public member
    double step_down_mm;
};

class Tool {
 public:
    double radius_mm() const { return 0.5 * diameter_mm_; }   // computes: earns it
};
```

The pair costs two functions, two names, and a layer of indirection, and delivers
exactly the access a public member gives. It also implies protection the class is
not providing, which misleads the next reader about where the invariant lives.
