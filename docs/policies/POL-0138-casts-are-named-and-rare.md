---
id: POL-0138
kind: standard
trigger: "write a cast"
attribution:
  - source: standard-practice
    locator: "casting"
    upstream: ["CG ES.48", "CG ES.49", "CG ES.50"]
---

# Avoid casts; where one is unavoidable, use the named cast and never cast away `const`

Prefer changing the type of the thing. Where a cast is genuinely needed, write
`static_cast` for a value conversion, `dynamic_cast` for a checked downcast, and
`reinterpret_cast` only at a foreign boundary with a comment. No C-style casts, and
no `const_cast`.

```cpp
const auto count = static_cast<int>(moves.size());
auto& grbl = dynamic_cast<GrblPost&>(post);

int count = (int)moves.size();                       // which cast is this?
auto* writable = const_cast<Tool*>(&tool);           // no
```

A C-style cast silently selects whichever of the four conversions compiles,
including `reinterpret_cast`, so the reader cannot tell which risk they are looking
at. Writing through a `const_cast` onto an object that was genuinely `const` is
undefined behaviour, and if the object was not `const`, the signature that said so
is the thing to fix.
