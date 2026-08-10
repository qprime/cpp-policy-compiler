---
id: POL-0015
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #2"
    upstream: ["CG C.2", "CG C.40", "CG C.41", "CG C.42"]
  - source: cpp-convention/mechanisms.md
    locator: "§7 Invariants and preconditions"
---

# Types with invariants establish them at construction

No object exists in an invalid state. A type whose members can vary
independently is a `struct`. A type with a constraint across its members is a
`class` whose constructor enforces that constraint and throws when it cannot be
met.

The test is a question about the data, not about encapsulation: is there a
combination of member values that must never exist? If yes, the constructor is
the only way in. If no, the type is an aggregate and wrapping it buys nothing
(POL-0042).

There is no `init()` a caller must remember to call, and no partially
constructed state to observe. A constructor either produces a valid object or
does not return.

POL-0022 carries how such a type is built, including the non-throwing
`try_from` form for callers that want to test rather than catch.

An invariant that is not established at construction is established by every
consumer instead, and each consumer chooses its own fallback for the invalid
case. Two sites that disagree produce two behaviours for one input, and nothing
connects them, so the divergence is invisible until the outputs are compared.
The constructor answers the question once, at the one place the object comes
into existence.
