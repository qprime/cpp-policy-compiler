---
id: POL-0056
kind: anti-pattern
replacement: [POL-0023]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: parallel near-duplicates"
---

# Never keep two functions that share most of their bodies

Two functions sharing more than half their bodies drift. A fix applied to one is
forgotten in the other, and nothing links them.

```cpp
// Never
Result compact_full(const Store& store, double min_fill);
Result compact_incremental(const Store& store, double min_fill);   // 40 of 50 lines identical

// Instead: one function, and the difference is a named field
Result compact(const Store& store, const CompactParams& params);   // params.mode
```

The test is whether a future change would have to be made in both places.
Accidental similarity that would not co-evolve stays separate, and merging it
produces a parameter that means nothing.

Duplication is cheap to create and its cost is entirely deferred. The two bodies
are identical on the day they are written, which is the only day anybody
compares them; from then on each is edited by whoever is working on its caller,
without cause to look at the other. The divergence is silent because both
compile and both pass their own tests, and it is found when two callers that
should agree do not.
