---
id: POL-0117
kind: guideline
attribution:
  - source: standard-practice
    locator: "control flow, statement selection"
    upstream: ["CG ES.70", "CG ES.72", "CG ES.73", "CG ES.75", "CG ES.77", "CG ES.85", "CG NR.2", "CG NR.6"]
---

# Control flow takes the plainest statement that fits

| Situation | Statement |
|-----------|-----------|
| Choosing among values of one variable | `switch` |
| An obvious loop variable | `for`, or range-`for` per POL-0099 |
| No obvious loop variable | `while` |
| A body that must run before the first test | Restructure; `do`-`while` is not written |

An early `return` is preferred to nesting, and there is no rule against several
of them. Cleanup rides on destructors (POL-0003), so no function needs a single
exit or a jump to a shared epilogue.

`break` and `continue` are permitted, sparingly, where they remove nesting the
reader would otherwise have to hold. An empty statement is written as `{}` on
its own line, never as a bare semicolon.

A `switch` over an enumeration is what makes an added enumerator a compile error
under POL-0033, which an `if`-chain over the same values will not do. The rest
of the table is uniformity: where two spellings are equally correct, taking the
common one costs nothing and removes a decision from every later edit
(POL-0004). A `do`-`while` inverts the reader's expectation that a loop tests
before it runs, which is why it is worth restructuring around rather than
spending attention on.
