---
id: POL-0013
kind: guideline
trigger: "write a routine the standard library already provides"
attribution:
  - source: standard-practice
    locator: "library preference"
    upstream: ["CG P.13", "CG ES.1", "CG SL.1", "CG SL.2"]
---

# Reach for the standard library before writing it yourself

Before writing a loop, look for the algorithm. Before writing a container, look
for the container. A hand-rolled version answers to you for correctness,
performance, and every future reader.

```cpp
const auto found = std::ranges::find_if(
    moves, [](const Move& move) { return is_cut(move); });

std::size_t i = 0;
for (; i < moves.size(); ++i) { if (is_cut(moves[i])) break; }   // same, unnamed
```

The standard library is specified, tested against every implementation, and
already known to the reader. A third-party library earns its place the same way
and carries a dependency cost the standard library does not.
