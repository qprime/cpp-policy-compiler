---
id: POL-0004
kind: principle
precedence: 4
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #4"
---

# Boring is a feature

Two language features rather than seven. Idiomatic rather than clever. Reach for
the construction a competent C++ engineer expects to find, not the one that
demonstrates the most about the language.

Where two spellings are equally correct, take the common one. Arbitrary
variation costs consistency and buys nothing.

Every feature reached for is a feature every later edit has to handle. Unusual
constructions widen the space of plausible continuations: the next change has
more ways to be written and fewer of them are consistent with what is already
there. Uniformity is what lets a large body of code be extended one piece at a
time without drift, and drift is not visible in any single line.
