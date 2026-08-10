---
id: POL-0030
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: named operation"
    upstream: ["CG F.1", "CG F.2", "CG F.3", "CG F.8", "CG F.56"]
---

# Named operation

A long function is usually several operations that have not been named. The
signal is not line count. It is whether the block can be named.

If a comment would explain a block, that block is a function and the comment is
its name.

```cpp
// Instead of one long compact() with four implicit phases:
std::vector<Segment> collect_live_segments(const Store& store);
std::optional<Segment> find_reclaim_candidate(const std::vector<Segment>& segments,
                                              double min_fill);
void emit_relocation(Journal& journal, const Segment& from, const Segment& to);
```

Prefer pure functions: same input, same output, no side effects. Those are the
ones testable in isolation and readable without their context. Avoid
unnecessary condition nesting; return early.

Decomposition is not the goal, and splitting a function that cannot be named
produces `compact_part_two`, which is worse than the original. The name is the
deliverable.

A named operation can be understood from its declaration, so the reader learns
what the code does without simulating it. An unnamed block can only be
understood by executing it mentally, and that reconstruction is where wrong
assumptions enter: the block shows what the code does and never what it was
required to do. Naming also fixes the boundary, which is what lets one phase be
replaced without re-reading the three around it.
