---
id: POL-0034
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: when a thing becomes a type"
    upstream: ["CG C.2"]
---

# When a thing becomes a type

Work down the list. Stop at the first match.

| Question | If yes |
|----------|--------|
| Does it have an invariant — some combination of values that must never exist? | A `class` with a validating constructor (POL-0015, POL-0022) |
| Does it have a *structural* precondition other code wants to assume? | A wrapper type (POL-0027) |
| Is it a fixed set of alternatives? | `enum class`, or a variant when the alternatives carry payloads (POL-0033) |
| Do several values always travel together into functions? | A params struct or an aggregate (POL-0023) |
| Are two same-typed values confusable at a boundary, *and* does arithmetic not flow through them? | A distinct type — a named escape, not the default (POL-0038) |
| None of the above | A primitive with a unit-suffixed name (POL-0017). This is the common case. |

The last row is the answer most of the time, and the list is ordered so that the
cheap answer is reached by elimination rather than by judgment. A question
skipped is a type introduced that carries no constraint, and a type with no
constraint is ceremony.

Every type is an interface somebody has to learn, so the question is never
whether a type would be tidier but whether it removes a way to be wrong. The
first four rows each name a specific wrongness the type makes unrepresentable.
Where no row matches, nothing is being prevented, and the primitive is what the
next reader already understands.
