---
id: POL-0038
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: how to pass a parameter"
    upstream: ["CG F.18"]
---

# A will-move-from parameter takes `X&&` and is moved from in the body

When a function's job is to take ownership of a concrete type, take `X&&` and
`std::move` it exactly once into its destination.

```cpp
class Toolpath {
 public:
    void adopt(std::vector<Move>&& moves) { moves_ = std::move(moves); }

 private:
    std::vector<Move> moves_;
};
```

Taking by value and moving works too and is simpler when the function always
stores the argument; `X&&` is for the case where the caller must see in the
signature that the value is consumed. Failing to move in the body silently turns
the whole thing into a copy with no diagnostic.
