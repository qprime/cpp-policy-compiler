---
id: POL-0020
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #10"
    upstream: ["CG P.10", "CG Con.1", "CG Con.2", "CG Con.3", "CG Con.4", "CG Con.5"]
  - source: cpp-convention/mechanisms.md
    locator: "§6 Immutability"
---

# `const` by default

Four sites, each `const` unless something requires otherwise:

| Site | Form |
|------|------|
| An object that does not change after construction | `const T x = ...;` |
| A member function that does not mutate | trailing `const` |
| A parameter that is only read | `const T&`, or `const T` by value |
| A value known at compile time | `constexpr` |

`constexpr` is the stronger claim and is preferred wherever the value can be
computed at compile time. `inline constexpr` at namespace scope in a header
requires C++17; a C++11 project puts a header constant in an anonymous namespace
or behind a function returning it. C++20 adds `consteval` for the case where
compile-time evaluation is required rather than merely possible.

A `const` member and a private member with a `const` accessor are both
immutable; choose by whether the type has an invariant to protect (POL-0015).

The order in which `const` is decided is the point: it is written first and
removed when a mutation is required, never added once the code is believed
correct. Written the other way, `const` records what happened to be true when
someone last looked, which is not a guarantee anything can rely on. A
non-`const` object tells the reader it changes, so an object that never changes
and is not marked makes that signal a lie everywhere in the file.
