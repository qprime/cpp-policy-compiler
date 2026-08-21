---
id: POL-0062
kind: standard
trigger: "define a type and declare a variable of it in one statement"
attribution:
  - source: standard-practice
    locator: "type definitions"
    upstream: ["CG C.7"]
---

# Define a type and declare its variables in separate statements

Close the type definition, then declare.

```cpp
struct Bounds {
    Vec2 min_mm;
    Vec2 max_mm;
};

Bounds stock_bounds;
```

```cpp
struct Bounds { Vec2 min_mm; Vec2 max_mm; } stock_bounds;   // no
```

The combined form buries a type definition where readers look for a variable, and
it makes the type unfindable by name in a grep for `struct Bounds {`.
