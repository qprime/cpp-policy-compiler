---
id: POL-0117
kind: guideline
trigger: "reach for a language feature where an abstraction exists"
attribution:
  - source: standard-practice
    locator: "levels of abstraction"
    upstream: ["CG ES.2"]
---

# Reach for the abstraction before the language feature

When a container, algorithm, or named type expresses what you mean, use it instead
of assembling the same behaviour out of loops, pointers, and casts.

```cpp
const bool any_cut = std::ranges::any_of(moves, is_cut);

bool any_cut = false;
for (std::size_t i = 0; i < moves.size(); ++i) {
    if (is_cut(moves[i])) { any_cut = true; break; }
}
```

The abstraction states the intent in its name and has no index to get wrong. Raw
language features are the right level only where no abstraction fits, and that is
rarer than it looks from inside the loop you are writing.
