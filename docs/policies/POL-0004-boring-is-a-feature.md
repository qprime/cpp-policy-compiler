---
id: POL-0004
kind: principle
precedence: 4
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #4"
---

# Boring is a feature

Given two forms that work, take the one the next reader already knows. Reach for
two language features rather than seven, and keep the reader inside the file.

```cpp
for (const Move& move : moves) { ... }                    // read and move on

std::for_each(moves.cbegin(), moves.cend(),
              [&](const auto& move) { ... });             // same work, more to know
```

Every feature you reach for is a feature the next reader must know before they
can change the line. Cleverness is a cost paid by everyone downstream of it and
recovered by no one.
