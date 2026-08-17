---
id: STD-0013
group: names
enforced_by: review
attribution:
  - source: standard-practice
    locator: "name length"
    upstream: ["CG NL.7", "CG ES.7", "CG ES.8"]
---

# Name length is proportional to scope

A loop index living three lines is `i`. A parameter living one function is a word.
A name visible across the project is spelled out.

```cpp
for (std::ptrdiff_t i = 0; i < std::ssize(rings); ++i) { ... }

double area_mm2(const ConvexPolygon& poly);

constexpr double kMinMarginMm = 10.0;
```

Two names in one scope differ by more than a digit or a lookalike character:
`ring1` and `ringl` is a transposition that compiles.
