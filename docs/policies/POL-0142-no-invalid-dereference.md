---
id: POL-0142
kind: standard
attribution:
  - source: standard-practice
    locator: "pointer validity"
    upstream: ["CG ES.65"]
---

# Establish that a pointer or iterator is valid before dereferencing it

Check against null where absence is possible; check against `end()` before
dereferencing a search result; do not hold an iterator across an operation that
may invalidate it.

```cpp
if (const auto it = std::ranges::find(moves, target); it != moves.end()) {
    use(*it);
}

auto it = moves.begin();
moves.push_back(extra);
use(*it);                                     // reallocation invalidated it
```

Dereferencing an invalid pointer or iterator is undefined behaviour, and the common
outcome is reading plausible data from freed storage rather than crashing. The
invalidation rules belong to each container, so the safe habit is to re-acquire the
iterator after any mutation.
