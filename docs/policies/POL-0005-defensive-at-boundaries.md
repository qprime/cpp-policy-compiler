---
id: POL-0005
kind: principle
precedence: 5
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #5"
    upstream: ["CG P.7"]
---

# Defensive at boundaries, trusting inside

Validate at the outside edge: user input, file parsing, FFI, anything arriving
from a system whose guarantees you do not control. Past that edge, trust what
was established.

If a precondition is checked in three places, the fix is a type that establishes
it once, not a fourth check.

Scattered internal checks are a missing invariant, not thoroughness. They drift
the moment one site's fallback differs from another's, which turns one absent
invariant into two different behaviours for the same input.
