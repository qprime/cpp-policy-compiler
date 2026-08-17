---
id: POL-0130
kind: standard
attribution:
  - source: standard-practice
    locator: "expression complexity"
    upstream: ["CG ES.40", "CG ES.41"]
---

# One expression does one thing, and precedence is parenthesized when it is not obvious

Split a compound expression into named intermediates. Where operators of different
kinds meet — arithmetic with shifts, comparison with bitwise — parenthesize even
if the precedence is right.

```cpp
const double r_eff_mm = 0.5 * (bore_d_mm - tool_d_mm);
const double margin_mm = r_eff_mm - kMinMarginMm;
if (margin_mm < 0.0) { ... }

if (0.5 * (bore_d_mm - tool_d_mm) - kMinMarginMm < 0.0 && !faces.empty()) { ... }
```

A long expression is a computation with no names in it, so a reader must
reconstruct the intermediate meanings the author already knew. Named intermediates
also give a debugger something to show and an error message somewhere to point.
