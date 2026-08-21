---
id: POL-0148
kind: standard
trigger: "declare or modify a loop variable"
attribution:
  - source: standard-practice
    locator: "loop variables"
    upstream: ["CG ES.74", "CG ES.86"]
---

# The loop variable is declared in the initializer and not modified in the body

Advance it only in the `for` header. Where the body needs to skip or repeat, change
the condition or use a different loop shape.

```cpp
for (std::ptrdiff_t i = 0; i < std::ssize(moves); ++i) { ... }

for (std::ptrdiff_t i = 0; i < std::ssize(moves); ++i) {
    if (is_arc(moves[i])) { i += 2; }            // the header now lies
}
```

Once the body advances the counter, the header no longer describes the traversal
and a reader has to simulate the loop to know which elements are visited.
Declaring the variable in the initializer also keeps it from outliving the loop and
being read afterwards.
