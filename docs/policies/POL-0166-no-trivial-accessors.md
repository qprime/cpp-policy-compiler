---
id: POL-0166
kind: guideline
attribution:
  - source: standard-practice
    locator: "accessors"
    upstream: ["CG C.131"]
---

# A getter-and-setter pair on every member means the type is a `struct`

```cpp
// Avoid. Six lines of ceremony to expose two public fields.
class Point {
 public:
    double x() const { return x_; }
    void set_x(double v) { x_ = v; }
    double y() const { return y_; }
    void set_y(double v) { y_ = v; }
 private:
    double x_{0.0};
    double y_{0.0};
};

// Prefer. Constraint-free data is an aggregate.
struct Point {
    double x{0.0};
    double y{0.0};
};
```

A read accessor with no matching setter is different and is fine: it exposes a
value while keeping the invariant, which is what POL-0022 asks for.

A settable pair on every member provides no encapsulation. Any caller can put
the object in any state, so there is no invariant, which means the private
members were never protecting anything — the class is an aggregate wearing
method calls (POL-0042).

It also costs at the point it matters most. A reader who sees a class assumes an
invariant and goes looking for it, and the accessors are what makes that search
take a while before coming up empty (POL-0006).
