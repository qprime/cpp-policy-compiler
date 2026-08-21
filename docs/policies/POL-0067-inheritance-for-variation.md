---
id: POL-0067
kind: anti-pattern
trigger: "write a class hierarchy for a fixed set of alternatives"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: inheritance for variation"
    upstream: ["CG C.129"]
replacement: ["POL-0066"]
---

# A class hierarchy standing in for a fixed set of alternatives

`class Move { virtual ~Move(); }` with `Rapid` and `Cut` deriving from it is a
v-table where a variant belongs.

```cpp
class Move {                                  // no
 public:
    virtual ~Move() = default;
    virtual std::string emit() const = 0;
};
```

Inherit only for an open set of behaviours behind an interface with no data. A
closed set gets no exhaustiveness check from a hierarchy: adding `Dwell` compiles
everywhere and is handled nowhere.
