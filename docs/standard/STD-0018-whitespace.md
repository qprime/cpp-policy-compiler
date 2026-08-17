---
id: STD-0018
group: layout-of-the-line
enforced_by: clang-format
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG NL.15"]
---

# Whitespace is whatever the formatter produces

Run the formatter; do not hand-align. No column-aligned assignments, no padded
comment blocks, no extra blank lines to group what a blank line already groups.

```cpp
const double step_over_mm = 6.0;
const double ramp_angle_deg = 30.0;

const double step_over_mm   = 6.0;      // no: realigns on the next rename
const double ramp_angle_deg = 30.0;
```

Hand alignment is undone by the next formatter run and, where the formatter is
disabled to preserve it, by the next name that is one character longer.
