---
id: POL-0160
kind: guideline
trigger: "change data layout for speed"
attribution:
  - source: standard-practice
    locator: "data layout"
    upstream: ["CG Per.16", "CG Per.17", "CG Per.18", "CG Per.19"]
---

# Once measurement says layout matters, make the data compact and walk it in order

Store what the hot loop reads next to what it reads now: contiguous containers,
the frequently-read members first, no padding you can remove by reordering. Do this
after a profile named the loop, not before.

```cpp
struct MoveHot {           // read every iteration
    Vec2 end_mm;
    double feed_mm_per_min;
};

struct MoveCold {          // read on emit only
    std::string comment;
    int source_line;
};
```

A cache miss costs a couple of hundred cycles, so on a loop that misses every
iteration the layout is the whole cost and the arithmetic is free. Space is time at
that scale. It is also invisible in the source, which is why it waits for a
measurement.
