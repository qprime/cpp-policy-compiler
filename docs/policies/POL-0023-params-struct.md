---
id: POL-0023
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: params struct"
    upstream: ["CG I.23", "CG I.24", "CG F.21"]
---

# Params struct

C++ has no keyword arguments, so a struct with designated initializers is how a
call site names what it is passing.

```cpp
// Wrong. Four adjacent doubles; every ordering compiles.
Result compact(const Store& store, double load_factor, double slack_ratio,
               double min_fill, double max_growth, CompactMode mode);

compact(store, 0.75, 0.10, 0.50, 2.0, CompactMode::Incremental);
//             ^^^^^^^^^^^^^^^^^^^^^ transpose any pair; still compiles
```

```cpp
// Right. Named fields at the construction site; no ordering to get wrong.
struct CompactParams {
    double load_factor;
    double slack_ratio;
    double min_fill;
    double max_growth;
    CompactMode mode = CompactMode::Full;
};

Result compact(const Store& store, const CompactParams& params);

compact(store, CompactParams{
    .load_factor = 0.75,
    .slack_ratio = 0.10,
    .min_fill = 0.50,
    .max_growth = 2.0,
    .mode = CompactMode::Incremental,
});
```

Designated initializers are C++20. On earlier standards the struct is still the
right shape: the fields are assigned to a named local before the call, or a
small builder produces it.

The same reasoning applies on the way out. A function with several outputs
returns a struct rather than taking out-parameters.

POL-0016 is the rule this satisfies, and it names the alternative route:
distinct types, which make a transposition ill-formed rather than merely
visible. Either is sufficient and neither requires the other.

A struct moves the parameter names from the declaration, where the caller cannot
see them, to the call, where the caller writes them. That converts an ordering
mistake from something the compiler accepts into something the author has to
type wrong on purpose. It also gives new parameters a place to arrive that does
not disturb existing call sites, so the interface can grow without a round of
edits that each risk the same transposition.
