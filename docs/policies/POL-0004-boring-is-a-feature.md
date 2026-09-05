---
id: POL-0004
kind: principle
precedence: 4
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #4"
---

# Boring is a feature

Given two equally correct and expressive forms, take the one the next reader is
more likely to know. Prefer a named standard algorithm when the algorithm is the
intent; prefer direct control flow when it says the same thing more clearly.

```cpp
for (const Move& move : moves) { ... }                    // read and move on

std::for_each(moves.cbegin(), moves.cend(),
              [&](const auto& move) { ... });             // same work, more to know
```

Every feature adds something the next reader must understand before changing
the line. Pay that cost when it supplies a real guarantee or communicates the
operation, not merely to compress familiar code.
