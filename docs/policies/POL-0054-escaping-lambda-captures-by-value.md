---
id: POL-0054
kind: standard
attribution:
  - source: testimony/coding-rules-2026-07.md
    locator: "Lambdas #3"
    upstream: ["CG F.52", "CG F.53"]
---

# A lambda that outlives its scope captures by value

By-reference capture is allowed only where the lambda runs and dies inside the
current scope — the comparator handed to an algorithm. Anything stored, returned,
or handed to another thread captures by value or takes explicit ownership.

```cpp
std::ranges::sort(moves, [&origin_mm](const Move& a, const Move& b) {
    return distance(a, origin_mm) < distance(b, origin_mm);   // dies here: fine
});

callbacks_.push_back([&job] { report(job); });      // job dies first: dangles
callbacks_.push_back([job] { report(job); });       // instead
```

A by-reference capture is a non-owning observer with no diagnostic when it
escapes. Capturing `this` is the same hazard wearing a different name: if the
callable outlives the object, every call dereferences a dead `this`.
