---
id: POL-0051
kind: anti-pattern
replacement: [POL-0008, POL-0021]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: blanket noexcept"
    upstream: ["CG E.12", "CG C.66"]
---

# Never apply `noexcept` as a blanket

`noexcept` is a claim about behaviour, not an annotation. Where the claim is
false the program calls `std::terminate`, with no unwinding and no handler.
"It is free" is wrong.

Write it where it is genuinely true and where it changes something:

- move constructor and move assignment (POL-0021)
- `swap`
- destructors, which are already `noexcept` by default
- functions doing pure arithmetic on built-in types

The blanket is attractive because the compiler accepts it everywhere and no test
fails. The claim is then checked at the one moment it matters, in production,
by terminating the process; a recoverable failure becomes an unrecoverable one
and the diagnostic that would have said why is exactly what was skipped. A
function marked `noexcept` also constrains every future edit to its body, and
nothing reminds the person making that edit that the constraint is there.
