---
id: POL-0018
kind: pattern
trigger: "write a function with a structural precondition"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: wrapper type for preconditions"
    upstream: ["CG I.5"]
---

# A structural precondition is carried by a wrapper type

A function whose precondition is structural — convex, sorted, non-empty, closed,
known winding — takes a type that proves it. The check happens once, where the
type is made.

```cpp
class ConvexPolygon {
 public:
    static std::optional<ConvexPolygon> try_from(Polygon points);
    const Polygon& points() const { return points_; }

 private:
    explicit ConvexPolygon(Polygon points);
    Polygon points_;
};

Polygon inset(const ConvexPolygon& poly, double offset_mm);
```

`inset`'s signature proves its precondition: a non-convex polygon cannot reach
it without passing through `try_from`. The alternative is re-checking convexity
on every call or trusting a comment.

Scalar preconditions do not get a wrapper — a positive width belongs on the type
that owns the width field. Reserve wrappers for structure.
