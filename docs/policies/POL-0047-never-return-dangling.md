---
id: POL-0047
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: how to pass a parameter"
    upstream: ["CG F.43"]
---

# Never return a pointer or reference to a local

Return by value. A reference return is only valid when it names something that
outlives the call — a member, an element of a container the caller owns, or
`*this`.

```cpp
const Bounds& bounds_of(const Polygon& poly) {
    const Bounds b = compute_bounds(poly);
    return b;                                   // dangles
}

Bounds bounds_of(const Polygon& poly) {
    return compute_bounds(poly);                // moves or elides; always valid
}
```

The dangling version often appears to work: the storage is untouched until
something else uses the stack. That is the worst failure mode, because it passes
review, passes tests, and breaks under an unrelated change.
