---
id: POL-0010
kind: guideline
attribution:
  - source: standard-practice
    locator: "avoidable work"
    upstream: ["CG P.9"]
---

# Do not waste time or space, but spend both before you spend clarity

Delete work that buys nothing: a copy of a value already owned, a container
built to be read once, an allocation inside a loop that could be hoisted. Stop
there until a measurement asks for more.

```cpp
for (const Polygon& ring : rings) {
    std::vector<Vec2> scratch;                  // allocates every iteration
    ...
}

std::vector<Vec2> scratch;
for (const Polygon& ring : rings) {
    scratch.clear();                            // one allocation, same clarity
    ...
}
```

Waste of this kind costs nothing to remove and no reader pays for its absence.
Anything past it is optimization and answers to measurement.
