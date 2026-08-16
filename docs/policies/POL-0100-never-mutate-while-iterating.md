---
id: POL-0100
kind: anti-pattern
replacement: [POL-0098]
attribution:
  - source: standard-practice
    locator: "iteration, iterator invalidation"
    upstream: ["CG ES.83"]
---

# Never insert into or erase from a container while iterating it

```cpp
// Never. erase() invalidates it; the next ++it is undefined.
for (auto it = moves.begin(); it != moves.end(); ++it) {
    if (it->is_empty()) { moves.erase(it); }
}

// Right. One pass, no invalidation to reason about.
std::erase_if(moves, [](const Move& m) { return m.is_empty(); });
```

Below C++20 the spelling is the erase-remove idiom,
`moves.erase(std::remove_if(moves.begin(), moves.end(), pred), moves.end())`.
Where elements must be added, build a second container and swap it in.

Invalidation rules differ per container, so the identical pattern is defined on
`std::list` and undefined on `std::vector`, and the code gives no sign of which
one it is. Worse, the undefined case usually appears to work: the freed
capacity is still mapped, so the loop completes and the corruption surfaces
somewhere else entirely. A whole-container operation states the intent and has
no iterator for the reader to track (POL-0098).
