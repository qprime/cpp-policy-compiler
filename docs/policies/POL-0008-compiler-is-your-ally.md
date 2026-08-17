---
id: POL-0008
kind: principle
precedence: 8
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #8"
    upstream: ["CG P.5"]
---

# The compiler is your ally

Spend the compiler's checking wherever it is available: strong types where they
matter, `enum class` always, `[[nodiscard]]` where the return value is the
point, `constexpr` where possible, `noexcept` where genuinely true, dispatch
that breaks the build when a case is added.

```cpp
[[nodiscard]] std::optional<ConvexPolygon> try_from(Polygon points);
```

Without `[[nodiscard]]`, discarding that return silently drops the only report
of failure the function makes. Each of these annotations converts a class of
review comment into a diagnostic, which is the only form of review that never
gets tired.
