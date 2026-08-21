---
id: POL-0057
kind: guideline
trigger: "pass or return several values that always travel together"
attribution:
  - source: standard-practice
    locator: "aggregating data"
    upstream: ["CG C.1"]
---

# Values that travel together become one type

When the same two or three values are passed, returned, and stored side by side,
give them a name. The trigger is repetition across signatures, not the count.

```cpp
struct Bounds {
    Vec2 min_mm;
    Vec2 max_mm;
};

Bounds bounds_of(const Polygon& poly);

void bounds_of(const Polygon& poly, double* min_x_mm, double* min_y_mm,
               double* max_x_mm, double* max_y_mm);
```

Once the group has a name, an operation on it has somewhere to live and a change
to its shape is one edit. Loose values force every signature to restate the
grouping and every caller to keep the order straight.
