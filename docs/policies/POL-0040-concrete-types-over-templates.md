---
id: POL-0040
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 3: concrete types over templates"
  - source: cpp-convention/conventions.md
    locator: "Tier 2: template parameters are constrained"
  - source: cpp-convention/conventions.md
    locator: "Divergences: CG T.10"
    upstream: ["CG T.10"]
  - source: cpp-convention/mechanisms.md
    locator: "§9 Generic code"
    upstream: ["CG T.10", "CG T.11", "CG T.120"]
---

# Concrete types over templates

Write the concrete type. Templatize on one of two triggers: a third concrete
caller forces it, or the alternative is a runtime-typed interface that loses
type checking.

A template parameter carries its constraint, spelled per the declared standard:

| C++11 | C++17 | C++20 |
|-------|-------|-------|
| `static_assert` in the body stating the requirement; SFINAE only where unavoidable | `if constexpr` and `static_assert` | A concept, or a `requires` clause |

On C++20 an unconstrained template parameter is incomplete. On earlier standards
a `static_assert` carries the same information to the reader and produces a
diagnostic at the right place; the concept is better because the compiler
enforces it at the call rather than at the instantiation.

Two callers are not a generalization, they are two callers. Generalizing from
two produces a parameterization shaped by a coincidence, and the third caller
then either fits by accident or forces the abstraction to be redone with three
callers already depending on it. Waiting costs one duplicated function and buys
the information that says which axis actually varies.
