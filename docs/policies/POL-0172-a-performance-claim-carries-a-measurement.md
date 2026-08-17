---
id: POL-0172
kind: standard
attribution:
  - source: standard-practice
    locator: "performance claims"
    upstream: ["CG Per.6"]
---

# A change made for performance carries the measurement that justified it

```cpp
// Never. A claim with no referent, and a departure from POL-0004 on its strength.
// Faster than std::unordered_map.
FlatMap<ToolId, Tool> by_id_;

// Right. The number, the workload, and the date.
// Flat layout: 2.4x faster lookup than std::unordered_map at n<=64,
// measured 2026-08-14 on the 12k-move planner benchmark.
FlatMap<ToolId, Tool> by_id_;
```

This is one of the cases POL-0112 admits a comment for: a reason that makes an
otherwise unusual choice legible. Without it the next reader sees a departure
from the boring option (POL-0004) with no way to tell whether it was justified,
and no basis for undoing it.

An unmeasured performance claim is untestable, so it cannot be wrong and cannot
be removed. It accumulates: the codebase fills with complexity that was added
for speed nobody demonstrated and nobody can now argue against.

Most performance rules are deliberately absent from this corpus, because
optimization is code-local and measured rather than decided in advance. This is
the rule that makes that position workable — the measurement is what turns a
local decision into one a later reader can evaluate.
