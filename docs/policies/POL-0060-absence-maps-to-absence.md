---
id: POL-0060
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions: absence maps to absence"
  - source: cpp-convention/mechanisms.md
    locator: "§1 Absence, FFI"
---

# Absence maps to absence across the boundary

The optional mechanism on one side is the optional mechanism on the other. The
empty optional is the host language's null, and nothing else is.

Three things follow:

- NaN never crosses. A NaN arriving at the seam is a defect to investigate, not
  a missing value (POL-0013).
- An empty collection does not signal failure. It means the collection is empty.
- A sentinel does not become a null at the binding. If the C++ side produced a
  sentinel, the defect is on the C++ side (POL-0009).

The binding layer converts the representation and never the meaning. Where the
C++ standard predates a standard optional, the project's optional form is what
the binding maps, on the same terms.

A seam is where two value spaces meet, so it is where an overloaded value gets
its second chance to be misread. A `-1` translated to null at the binding gives
the host a clean-looking interface over a C++ signature that still admits the
sentinel everywhere else, which means the ambiguity survives and only the symptom
was hidden. Mapping absence to absence and nothing else keeps the seam a
translation rather than a repair.
