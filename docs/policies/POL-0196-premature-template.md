---
id: POL-0196
kind: anti-pattern
trigger: "reach for a template parameter list"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: premature template"
    upstream: ["CG T.120"]
replacement: ["POL-0195"]
---

# `template<...>` as the first reach

```cpp
template <class Face, class Tool>                 // one call site, both concrete
Paths plan_pocket(const Face& face, const Tool& tool, double step_over_mm);
```

The example has no demonstrated generic requirement: it has one caller and both
types are known. A template can provide strong checking, especially when
constrained, but it moves checking and diagnostics to instantiation and commonly
requires its definition to be visible there. Pay that cost for real genericity,
not in anticipation of hypothetical callers.
