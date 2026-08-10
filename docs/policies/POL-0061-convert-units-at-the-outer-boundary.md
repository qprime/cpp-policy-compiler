---
id: POL-0061
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions: units survive the trip"
---

# Unit conversion happens at the outer boundary, never at the FFI seam

A value arriving from user input or a parsed file is converted to the project's
internal unit there, at the outer edge. It crosses the FFI seam in that unit,
with its suffix intact (POL-0017), and the binding layer converts nothing.

```
user input / file  →  convert here, once
FFI seam           →  carry through unchanged
```

Converting at the seam is a category error. The seam is a language boundary, and
a unit is not a property of a language.

A conversion at the seam is invisible to both sides. The C++ side sees a value
in its own unit and the host side sees a value in its own unit, and neither
declaration says a factor was applied in between, so a value that takes a
different path into the system arrives unconverted and is indistinguishable.
Converting at the outer boundary puts the factor at the one place where the
value's unit is genuinely unknown, which is also the one place a wrong unit can
be reported to whoever supplied it.
