---
id: POL-0152
kind: guideline
attribution:
  - source: standard-practice
    locator: "naming, length and scope"
    upstream: ["CG ES.7", "CG ES.8", "CG NL.7"]
---

# A name is as long as its scope is wide

```cpp
// Right. Two lines of scope; the short name is readable in place.
for (const auto& m : moves) { total += m.length_mm(); }

// Right. Namespace scope; the name carries its meaning to a distant reader.
constexpr double kMinimumFinishingPassDepthMm = 0.2;
```

A loop index or a lambda parameter visible for three lines is short. A namespace
constant, an exported function, or a member read from anywhere in the class
spells its meaning out. Unit suffixes are required regardless of length
(POL-0017).

Names that differ only in case, only by a digit, or only by a transposition are
not written. `count1` and `countl`, `source` and `Source`, `set_x` and `setx` —
each pair reads identically in review and compiles differently.

Length is how a name pays for the distance between its declaration and its use.
A reader who can see the declaration needs no reminder of what it means; a
reader who cannot has only the name. Long names in a tight scope cost the same
attention as short names in a wide one, in the other direction — the line stops
being readable at a glance and the mechanism buries the intent (POL-0006).
