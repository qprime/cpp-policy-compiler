---
id: POL-0020
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: wrapper type for preconditions"
    upstream: ["CG I.7"]
---

# A postcondition the caller relies on is encoded in the return type

When a caller must know something about a result, return a type that says it
rather than documenting it. Reserve prose for postconditions no type can carry.

```cpp
std::optional<ConvexPolygon> hull_of(const Polygon& points);
Polygon hull_of(const Polygon& points);   // "result is convex" lives in a comment
```

The first signature hands the caller a fact the compiler will keep. The second
hands them a promise that survives exactly as long as the comment does.
