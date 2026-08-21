---
id: POL-0139
kind: guideline
trigger: "write an index into a loop"
attribution:
  - source: standard-practice
    locator: "bounds safety"
    upstream: ["CG ES.55", "CG SL.con.3"]
---

# Shape the code so there is no index to check

Iterate the container, take a view, or use an algorithm. Where an index is
unavoidable, derive it from the container rather than from arithmetic.

```cpp
for (const Move& move : moves) { ... }
const double total = std::ranges::fold_left(lengths, 0.0, std::plus{});

for (std::size_t i = 0; i <= moves.size(); ++i) { use(moves[i]); }   // off by one
```

An index that never exists cannot be out of range, so the check is not needed
rather than merely passing. Every hand-written bound is a place for an off-by-one
that `operator[]` will not report.
