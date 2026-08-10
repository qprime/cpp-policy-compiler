---
id: POL-0016
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #4"
    upstream: ["CG I.23", "CG I.24"]
  - source: cpp-convention/conventions.md
    locator: "Pattern: params struct"
---

# Interfaces do not admit silent reordering

No two adjacent parameters may be interchangeable: swappable by a caller,
changing what the call means, and drawing no complaint from the compiler. Keep
argument counts low.

Two triggers, either one sufficient:

- more than four parameters, regardless of their types
- two adjacent parameters of the same type, regardless of the count

Two routes satisfy the rule, and only one is required. Name the parameters, by
moving them into a params struct (POL-0023). Or make a transposition
ill-formed, by giving the confusable parameters distinct types (POL-0038 bounds
when that is worth its cost).

The escape is a genuinely conventional mathematical order that a reader would
be surprised to see disturbed: `lerp(a, b, t)`, `clamp(v, lo, hi)`,
`atan2(y, x)`. A struct does not improve these.

The defect is not the argument count. It is that the compiler cannot tell a
correct call from a transposed one, so the mistake survives compilation, review,
and any test whose inputs happen to be symmetric. Argument order is decided at
each call site and re-decided at every site added later, which makes the number
of chances to get it wrong grow with the number of callers rather than staying
fixed at one.
