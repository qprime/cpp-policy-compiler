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

Spend the compiler's checking where it expresses a real contract: strong types
where distinctions matter, scoped enumerations unless implicit conversion or C
interop is intentional, `[[nodiscard]]` where discarding the result is probably
a defect, `constexpr` when constant evaluation is useful, `noexcept` where
genuinely true, and dispatch that diagnoses an unhandled case.

```cpp
[[nodiscard]] std::optional<ConvexPolygon> try_from(Polygon points);
```

Without `[[nodiscard]]`, discarding that return silently drops the only report
of failure the function makes. Use language and type-system checks to turn
enforceable contracts into repeatable diagnostics rather than recurring review
comments.
