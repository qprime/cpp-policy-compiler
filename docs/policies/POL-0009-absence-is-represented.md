---
id: POL-0009
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #3"
    upstream: ["CG F.60", "CG P.6"]
  - source: cpp-convention/mechanisms.md
    locator: "§1 Absence"
---

# Absence is represented, never encoded

A value that may legitimately not be there is represented by something whose
type says so. Encoding it in the value space instead is POL-0013, which
enumerates the forms that takes.

The intent is universal. The mechanism depends on the standard the project
declares, and reaching for a mechanism from a later column than the declared one
is a defect.

| C++11 | C++17 | C++20 |
|-------|-------|-------|
| No standard mechanism. Two permitted forms: a dedicated `Optional<T>`-alike in the project's support header, or a `bool`-returning `try_*` function with a reference out-parameter at a documented boundary. Pick one per project; do not mix. | `std::optional<T>` | `std::optional<T>` |

Columns group standards where the grouping changes no guidance: the C++11 column
covers C++11 and C++14, the C++20 column covers C++20 and C++23.

Absence is not failure. The optional form means there is legitimately nothing
here. A failure carrying a reason the caller must act on uses the result
mechanism instead, and substituting one for the other discards the reason.

Once absence shares a representation with a legal value, the type system cannot
separate them again, and every site downstream inherits the ambiguity without
any way to detect that it did.
