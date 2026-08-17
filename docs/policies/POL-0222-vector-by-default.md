---
id: POL-0222
kind: standard
attribution:
  - source: standard-practice
    locator: "container selection"
    upstream: ["CG SL.con.2"]
---

# The default container is `std::vector`

Reach for something else when a measurement or a required operation says so:
`std::array` for a compile-time size, `std::map` when ordered iteration is part of
the output, `std::unordered_map` for lookup where iteration order never escapes,
`std::deque` when you push at both ends.

```cpp
std::vector<Move> moves;                        // default
std::map<std::string, Layer> layers;            // iteration order is emitted
```

A `vector` is contiguous, so iteration is a cache-friendly walk and the element
access has no indirection; `std::list` and `std::set` pay a pointer chase per
element and usually lose even at the operation they were chosen for. Choosing
`vector` first also means the container appears in profiles rather than in guesses.
