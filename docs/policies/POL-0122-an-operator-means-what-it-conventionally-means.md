---
id: POL-0122
kind: standard
attribution:
  - source: standard-practice
    locator: "operator overloading, meaning"
    upstream: ["CG C.160", "CG C.162", "CG C.163", "CG C.167", "CG C.166"]
---

# An operator is defined only for its conventional meaning

```cpp
// Never. + does not mean "append a move to a plan".
Plan operator+(const Plan& p, const Move& m);

// Right. The operation has a name.
Plan with_move(const Plan& p, const Move& m);

// Right. Arithmetic on a dimensioned value is what + means.
constexpr Millis operator+(Millis a, Millis b) { return Millis{a.count() + b.count()}; }
```

Overload only across operations that are genuinely equivalent — the same
operation on different argument types. Two overloads of one operator that do
different things are two operations sharing a name, which is the case a name
exists to distinguish (POL-0006).

`operator&` is overloaded only as part of a smart pointer or reference system,
and `operator->` only on a type that stands in for a pointer.

An operator is a name whose meaning the reader already knows, which is the
entire value of using one. A `+` that appends, a `<<` that does anything but
stream or shift, an `operator bool` on a type that is not a truth value — each
spends the reader's existing knowledge to buy brevity, and the reader has no
way to discover the substitution except by opening the definition. A named
function costs the same keystrokes and states what it does (POL-0030).
