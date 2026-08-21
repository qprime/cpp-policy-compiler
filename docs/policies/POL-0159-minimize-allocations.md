---
id: POL-0159
kind: guideline
trigger: "allocate inside a loop"
attribution:
  - source: standard-practice
    locator: "allocation cost"
    upstream: ["CG Per.14"]
---

# Allocate outside the loop, and reserve when the size is known

Hoist a scratch buffer out of a loop and `clear()` it. Call `reserve` when the final
count is known or bounded.

```cpp
std::vector<Vec2> points;
points.reserve(expected_count);
for (const Polygon& ring : rings) {
    points.clear();
    append_ring(points, ring);
    emit(points);
}
```

Each allocation is a call into the allocator plus a copy of everything already in
the container when a `vector` grows. Removing them from a loop costs no clarity,
which is what separates this from optimization that answers to measurement.
