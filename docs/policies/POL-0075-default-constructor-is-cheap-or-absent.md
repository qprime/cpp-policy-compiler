---
id: POL-0075
kind: guideline
trigger: "write a default constructor"
attribution:
  - source: standard-practice
    locator: "default construction"
    upstream: ["CG C.43", "CG C.44"]
---

# A default constructor produces a meaningful empty value, cheaply and without throwing

Provide one when the type has a natural empty or zero state, and make it trivial.
Where no such state exists, leave it out and let the invariant-carrying
constructor be the only way in.

```cpp
struct Bounds {
    Vec2 min_mm;                 // default: the empty bounds, no work
    Vec2 max_mm;
};

class Tool { public: Tool(double diameter_mm, double rpm); };   // no default: none exists
```

A default constructor that allocates, reads a file, or throws makes every
container resize and every two-phase initialization a failure point. A default
constructor that fabricates a fake value — a zero-diameter tool — is worse,
because it hands out an object the invariant was supposed to forbid.
