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

Strong types where they matter, `enum class` always, `[[nodiscard]]` where the
return value is the point, `constexpr` where possible, `noexcept` where
genuinely true, exhaustive dispatch that breaks compilation when a case is added.

Prefer the construction that makes a future mistake fail the build over the one
that makes it fail a test, and prefer either over the one that makes it fail in
the field.

The compiler is the one check present every time the code is built, on every
platform, with nothing to have been kept current and nobody to have remembered
to run it. Work moved into it is work that cannot be skipped.
