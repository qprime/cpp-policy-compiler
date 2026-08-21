---
id: POL-0215
kind: standard
trigger: "write a type that must satisfy a concept"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "9. Generic code"
    upstream: ["CG T.150"]
---

# A type that must satisfy a concept says so with a `static_assert` beside it

Put the assertion next to the class definition, so the check happens at the
definition rather than at the first use.

```cpp
class GrblPost final : public PostProcessor { ... };
static_assert(Emitter<GrblPost>, "GrblPost must satisfy Emitter");
```

Without it, a type that stops satisfying the concept — a member renamed, a `const`
dropped — fails at whichever call site instantiates the template, which may be in
another target and may be a long way from the change. The assertion moves the report
to the file that broke it.
