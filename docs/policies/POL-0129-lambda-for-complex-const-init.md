---
id: POL-0129
kind: guideline
trigger: "compute a const value in several steps"
attribution:
  - source: standard-practice
    locator: "complex initialization"
    upstream: ["CG ES.28"]
---

# Where a `const` value takes several steps to compute, initialize it with an immediately-invoked lambda

```cpp
const std::vector<Polygon> rings = [&] {
    std::vector<Polygon> built = build_inset_rings(face, step_over_mm);
    std::ranges::sort(built, by_area);
    built.erase(drop_slivers(built), built.end());
    return built;
}();
```

The alternative is declaring the variable non-`const`, mutating it into shape, and
leaving it non-`const` forever — so nothing downstream can tell that the building
phase is over. The lambda confines the mutation to the initializer and hands back
a value that is `const` from its first use.

Keep it to a few lines. Past that it is a named function.
