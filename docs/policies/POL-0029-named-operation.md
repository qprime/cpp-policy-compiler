---
id: POL-0029
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: named operation"
    upstream: ["CG F.1", "CG F.2", "CG F.3", "CG F.10", "CG T.140"]
---

# An operation worth doing is worth a name

The signal is not line count, it is whether you can name what a block does. If a
comment would explain the block, that block is a function and the comment is its
name. One function, one logical operation.

```cpp
// Instead of one 90-line plan_pocket_spiral with four implicit phases:
std::vector<Polygon> build_inset_rings(const ConvexPolygon& outermost,
                                       double step_over_mm);
std::optional<Span> find_sliver_span(const Polygon& innermost,
                                     double tool_diameter_mm);
void emit_ring_transition(Path& moves, const Polygon& from, const Polygon& to);
```

A long function is usually several operations nobody named. Naming them is how
the reader learns what the code does without simulating it, and it is what makes
each phase testable on its own.
