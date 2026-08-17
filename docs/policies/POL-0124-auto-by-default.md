---
id: POL-0124
kind: anti-pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: auto by default"
    upstream: ["CG ES.11"]
replacement: ["POL-0123"]
---

# `auto` on every declaration

```cpp
auto result = compute_clearance(stock, part);   // double? Bounds? optional?
auto count = moves.size();                      // signed? unsigned? which width?
```

The reader now has to open `compute_clearance` to learn what they are holding, and
a change to its return type silently changes every downstream expression. `auto`
against redundancy is the rule; `auto` against naming types deletes the
information a declaration exists to carry.
