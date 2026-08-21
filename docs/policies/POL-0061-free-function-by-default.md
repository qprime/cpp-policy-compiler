---
id: POL-0061
kind: pattern
trigger: "decide whether a function is a member"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: free function by default"
    upstream: ["CG C.4", "CG C.5"]
---

# A function becomes a member only when it needs the representation

If the function can be written against the public interface, write it as a free
function in the same namespace as the type.

```cpp
class ConvexPolygon { /* only what needs the representation */ };

Polygon inset(const ConvexPolygon& poly, double offset_mm);
double area_mm2(const ConvexPolygon& poly);
Bounds bounds_of(const ConvexPolygon& poly);
```

A member function is part of the interface, and the interface should be as small
as the invariant requires. Free functions keep the class small enough to audit,
let algorithms be added without touching it, and mean a bug in `area_mm2` cannot
corrupt the invariant. Same namespace, so lookup finds them the way it finds
members.
