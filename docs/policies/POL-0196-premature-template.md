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

Nothing about the function is generic: it has one caller and both types are known.
What the template bought is the loss of type checking at the declaration, error
messages that appear in the caller's translation unit, and a definition that must
live in a header.
