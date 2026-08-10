---
id: POL-0041
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 3: public API is validated; internals trust their contracts"
---

# Public API is validated; internals trust their contracts

Validation happens where untrusted values enter: a public entry point, a parsed
file, user input, an FFI seam. Past that edge, internal helpers trust what was
established and do not re-check it.

Where a check is genuinely load-bearing inside, it becomes a type rather than a
repeated test (POL-0027). Where it is a "cannot happen" restatement, it is an
`assert` and nothing more.

The named escape is the FFI layer, which converts and validates at the seam and
is permitted the boilerplate that implies (POL-0064). Document it as the
boundary it is.

Internal re-validation is not defence in depth, because the second check has no
more information than the first and no way to do anything different with a
failure. What it does have is its own idea of what to do when the value is bad,
and two such ideas in one call chain produce two behaviours for one input
(POL-0045). Concentrating validation at the boundary is what makes the boundary
findable later, when the question is where a bad value could have entered.
