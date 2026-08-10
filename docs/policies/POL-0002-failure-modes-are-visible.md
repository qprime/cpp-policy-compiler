---
id: POL-0002
kind: principle
precedence: 2
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #2"
    upstream: ["CG P.6", "CG P.7"]
---

# Failure modes are visible

Errors are not swallowed. Invalid states are unrepresentable where possible and
rejected at construction where not. A function that cannot do what it was asked
says so; it does not return a plausible value.

A loud failure at the point of the mistake is always preferable to a quiet one
that survives.

A silent wrong answer is the worst possible failure, because nothing downstream
can tell it from a right one. Where output is consumed by another program, a
device, or a later build step rather than read by a person, there is no stage at
which the error becomes visible on its own. It is acted on, and the cost lands
far from the code that caused it.
