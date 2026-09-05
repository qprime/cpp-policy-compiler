---
id: POL-0124
kind: anti-pattern
trigger: "write auto on every declaration"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: auto by default"
    upstream: ["CG ES.11"]
replacement: ["POL-0123"]
---

# `auto` on every declaration

```cpp
auto result = compute_clearance(stock, part);   // double? Bounds? optional?
auto clearance = compute_clearance(stock, part); // type carries domain meaning
```

The reader now has to open `compute_clearance` to learn what they are holding, and
a change to its return type silently changes every downstream expression. `auto`
against redundancy is the rule; `auto` against naming types deletes the
information a declaration exists to carry. Keep `auto` where the initializer
already states the type, where the exact type is deliberately coupled to an API
(such as `container.size()`), or where the type is impractical to spell.
