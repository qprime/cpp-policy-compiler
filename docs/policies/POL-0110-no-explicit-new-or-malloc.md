---
id: POL-0110
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "3. Ownership"
    upstream: ["CG R.10", "CG R.11", "CG ES.60", "CG ES.61"]
---

# No explicit `new`, `delete`, `malloc`, or `free`

Use a value, a container, or `std::make_unique`. The only `new` in the codebase is
inside a resource-owning type that cannot be expressed any other way, paired with
its `delete` in the same class.

```cpp
std::vector<Move> moves(count);                          // yes
auto post = std::make_unique<GrblPost>(dialect);         // yes

Move* moves = new Move[count];                           // no
Move* moves = static_cast<Move*>(std::malloc(bytes));    // no
```

Every explicit `new` is a `delete` somebody has to remember on every path out,
including the ones that throw. `malloc` additionally skips construction, so the
returned storage holds no objects and destroying it skips destruction too.

`delete[]` pairs with `new[]` and `delete` with `new`; mixing them is undefined
behaviour, and the way to never mix them is to write neither.
