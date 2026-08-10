---
id: POL-0019
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #9"
    upstream: ["CG P.4", "CG ES.20"]
---

# No undefined behaviour, no run-to-run variation

Four things are defects, each on its own:

- undefined behaviour of any kind, whatever the observed result
- unordered-container iteration order reaching output
- reading an object before it is initialized
- platform-dependent floating-point in output that is compared

Where iteration order reaches output, the fix is an ordered container or an
explicit sort at the point of emission, not a hash seed that happens to be
stable. Where floating-point reaches compared output, the fix is a stated
tolerance or a fixed-precision rendering, not a hope that two toolchains agree.

Every object is initialized at the point of declaration. `const` (POL-0020)
forces this, which is one more reason it is the default.

Undefined behaviour is not a wrong answer, it is the absence of any contract
about the answer. Code that appears to work under one compiler, one
optimization level, and one input has not been shown to work at all; it has been
shown not to have been caught. Run-to-run variation costs the same thing from
the other direction: an output that differs between runs cannot be diffed
against a known-good one, so every mechanism that would have caught the next
defect stops working at once.
