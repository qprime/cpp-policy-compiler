---
id: POL-0156
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG Per.1", "CG Per.2", "CG Per.3", "CG Per.4", "CG Per.5", "CG Per.6"]
---

# Optimize only what a measurement named

Write the clear version. When something is too slow, profile it, change the thing
the profile named, and measure again. State the numbers in the commit message.

```cpp
// plan_pocket: 4.2s -> 0.9s on the 1200-face bench; the profile named
// build_inset_rings, which was re-offsetting the outer ring per pass.
std::vector<Polygon> build_inset_rings(const ConvexPolygon& outermost,
                                       double step_over_mm);
```

Intuition about where time goes is wrong often enough that acting on it usually
costs clarity and buys nothing. Complicated code and low-level code are not faster
by nature — the optimizer works best on the simple forms, and hand-written
cleverness routinely defeats it.

A performance claim with no number attached is not a claim anyone can check.
