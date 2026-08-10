---
id: POL-0001
kind: principle
precedence: 1
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #1"
    upstream: ["CG P.4", "CG P.5"]
---

# Correct by construction beats correct by test

The best defect is the one the type system refuses to compile. The second best
is the one a constructor rejects at the boundary. Tests confirm what the design
already guarantees; they are due diligence, not the correctness mechanism.

When two designs are otherwise equal, take the one that turns a class of mistake
into a compile error.

A codebase that relies on its test suite for correctness has moved the invariant
out of the code and into a process. That process runs after the code exists, if
it runs at all, and only over the cases someone thought to write. The compiler
runs against the code as written, every time.
