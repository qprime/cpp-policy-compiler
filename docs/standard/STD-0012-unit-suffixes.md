---
id: STD-0012
group: names
enforced_by: review
review_trigger: "a numeric interface omits the unit from its type or name"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #5"
    upstream: ["CG I.4", "CG NL.19"]
---

# A dimensioned value carries its unit in its type or name, at every interface

```cpp
double width_mm;
double feed_mm_per_min;
double angle_deg;
double duration_s;

double width;              // no
double feed;               // no
```

For primitive numeric representations, the suffix is the unit, spelled out,
lowercase, underscore-joined: `_mm`, `_deg`, `_s`, `_mm_per_min`, `_mm2` for
area. It appears on functions that return a primitive, parameters, members, and
struct fields. A strong unit type carries that information without repeating the
unit in every variable name.

Every primitive-valued interface carries the suffix, because an omitted boundary
is where unit transposition becomes possible.
