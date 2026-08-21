---
id: POL-0122
kind: guideline
trigger: "introduce a name close to one already in scope"
attribution:
  - source: standard-practice
    locator: "name distinguishability"
    upstream: ["CG ES.8"]
---

# Two names in the same scope differ by more than a character

When two names in view differ only by a digit, a plural, or a lookalike character,
rename one for what distinguishes it.

```cpp
const Polygon& outer_ring = rings.front();
const Polygon& inner_ring = rings.back();

const Polygon& ring1 = rings.front();
const Polygon& ringl = rings.back();       // l versus 1
```

A transposition between similar names compiles and type-checks, so it is found by
reading rather than by tooling. Names that differ by their meaning make the
mistake visible at a glance.
