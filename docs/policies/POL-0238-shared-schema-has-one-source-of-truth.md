---
id: POL-0238
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# A structure shared across the boundary has one schema and one source of truth

Move IR, parsed layouts, plan output — anything both sides construct or read — is
defined once. A change to it is versioned and lands as one commit: define, expose
across the boundary, document, regenerate the goldens, in that order.

```cpp
// ir/move.hpp — the source of truth for the move schema, v3
struct Move {
    Vec2 end_mm;
    double feed_mm_per_min;
    std::optional<double> dwell_s;        // added in v3
};
```

Two hand-maintained definitions of one structure agree until the first change, and
the disagreement shows up as a field silently reading zero rather than as a build
error. Versioning is what lets a reader tell an intentional schema change from a
regression when the goldens move.
