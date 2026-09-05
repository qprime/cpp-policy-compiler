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

Use inheritance when substitutable runtime polymorphism is the required model,
including genuinely open extension points. For a closed sum of alternatives, a
hierarchy alone provides no exhaustiveness check: adding `Dwell` can compile
without forcing every consumer to handle it.
