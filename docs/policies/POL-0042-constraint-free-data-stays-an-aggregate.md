---
id: POL-0042
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 3: class with a constructor for types with invariants"
    upstream: ["CG C.2"]
---

# Constraint-free data stays an aggregate `struct`

Where the members can vary independently, the type is a `struct` with public
members and default member initializers. No constructor, no accessors, no
`private`.

```cpp
struct Extent {
    double width_px = 0.0;
    double height_px = 0.0;
};
```

The test is whether some combination of member values must never exist. A
coordinate pair, a colour triple, and a configuration bag of independent fields
all fail that test, so all three stay aggregates. POL-0015 is the rule; this is
its escape, and the escape is where most data types land.

Accessors that return a member and a constructor that assigns its arguments
protect nothing. They add a file's worth of code between the reader and the
data, and they cost the aggregate initialization that would otherwise make a
construction site self-describing (POL-0023). Encapsulation is bought to protect
an invariant, so where there is no invariant the purchase is all cost.
