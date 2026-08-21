---
id: POL-0146
kind: standard
trigger: "write a loop over a whole container"
attribution:
  - source: standard-practice
    locator: "loop selection"
    upstream: ["CG ES.71"]
---

# Walking a whole container is a range-`for`

Bind `const auto&` to read, `auto&` to modify in place, and a value only where the
element is small and you want a copy. Reach for an index only when you need the
index itself.

```cpp
for (const Move& move : moves) { emit(move); }
for (Move& move : moves) { offset(move, delta_mm); }

for (std::size_t i = 0; i < moves.size(); ++i) { emit(moves[i]); }
```

The range form has no bound to state and no index to get wrong, and it works
unchanged if the container type changes. The index form restates the traversal on
every loop and is where off-by-one errors live.
