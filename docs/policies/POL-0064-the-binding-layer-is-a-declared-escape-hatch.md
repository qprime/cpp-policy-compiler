---
id: POL-0064
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions: the binding layer is a declared escape hatch"
  - source: cpp-convention/conventions.md
    locator: "Tier 3: public API is validated, FFI escape"
---

# The binding layer is a declared escape hatch

The binding layer converts, validates, and translates at the seam, and is
permitted the boilerplate that implies. It is the one place where boundary
ceremony is correct rather than a symptom.

What the escape covers: repeated conversion code, explicit validation of values
the C++ side would otherwise trust, raw-pointer handling dictated by a foreign
signature (POL-0046), and exception translation (POL-0059).

What it does not cover: business logic. A binding layer that computes anything is
no longer a binding layer, and the computation it acquired is now untested on
both sides.

Declare it as the boundary it is, in the file that implements it. The escape is
named so that the ceremony reads as deliberate rather than as an example to
follow.

Every rule the escape suspends was justified by an invariant established
elsewhere, and at the seam none of them has been established yet. Ceremony there
is the work of establishing them, which is why it is correct in exactly one file
and a defect in the next one over. Naming the file is what keeps the pattern from
spreading: without the declaration, the next author reads defensive conversion
code as the local convention and writes more of it inward.
