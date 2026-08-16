---
id: POL-0033
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: when a thing becomes a type, fixed set of alternatives"
  - source: cpp-convention/conventions.md
    locator: "Tier 2: closed-set variation"
  - source: cpp-convention/mechanisms.md
    locator: "§2 Closed-set variation"
    upstream: ["CG C.181", "CG C.182"]
---

# Closed-set variation is compiler-checked for exhaustiveness

A value that is one of a fixed set of alternatives is represented so that adding
an alternative breaks compilation at every site that must handle it. Falling
through silently is the defect this rule exists to prevent.

The intent is universal. The mechanism depends on the standard the project
declares.

| C++11 | C++17 | C++20 |
|-------|-------|-------|
| `enum class` tag plus a `switch` with **no `default` label**, compiled under `-Werror=switch`. Payload lives in a struct per alternative and the tagged aggregate is documented as a unit. | `std::variant` plus `std::visit` over an exhaustive overload set | `std::variant` plus `std::visit` |

The C++11 form is not a weaker version of the C++17 one. It obtains the same
guarantee from the warning system rather than from the type system, which is why
`-Werror=switch` is load-bearing rather than stylistic on a C++11 project.

One overload per alternative, never a generic `[](auto&&)` catch-all. A catch-all
compiles for every alternative added later and swallows exactly the case that
was just introduced, which removes the only property the variant was chosen for.

Forbidden in every standard: an `enum` paired with an if/else-if chain, which
obtains no guarantee at all, and a string tag field with optional payload members
(POL-0043).

A missing case is not detectable from the site that is missing it, because
nothing there is wrong. It is detectable only from the set of alternatives, which
lives somewhere else and grows without notifying anybody. Making exhaustiveness a
compile error moves the check from whoever remembers the alternative was added to
the build, which runs against every site every time.
