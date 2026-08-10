---
id: POL-0006
kind: principle
precedence: 6
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #6"
    upstream: ["CG P.1", "CG P.3"]
  - source: cpp-convention/conventions.md
    locator: "Naming: prefer a name over a comment"
    upstream: ["CG NL.1"]
---

# Express intent, not mechanism

The reader should see what the code means before how it works. A named operation
that says what it produces beats an inline block that computes it. A type that
names a constraint beats a comment stating it.

If the body must be opened to learn what a function is for, the name is the
defect. Where a comment would state what the code means, the name states it
instead.

Code that states its intent can be extended from its declaration. Code that
states only its mechanism has to be re-derived from its body before it can be
changed, and re-derivation is where wrong assumptions enter: the body shows what
the code does, never what it was required to do.
