---
id: POL-0035
kind: guideline
attribution:
  - source: testimony/coding-rules-2026-07.md
    locator: "Lambdas #1"
    upstream: ["CG F.11", "CG F.50", "CG T.141"]
---

# Prefer a named function; a lambda is for trivial glue at one call site

Write a lambda when it is short, used once, and reads better inline than as a
jump to a name. If it wants a name, a doc comment, or a second use, it is a
function.

```cpp
std::ranges::sort(moves, [](const Move& a, const Move& b) {
    return a.start_mm.x < b.start_mm.x;
});

bool is_reachable(const Move& move, const Envelope& envelope);   // named: reused, testable
```

A lambda buys locality, not brevity. Past a few lines it costs the reader the
name that would have told them what the block is for, and it cannot be tested
without the call site that holds it.
