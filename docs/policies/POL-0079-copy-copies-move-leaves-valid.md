---
id: POL-0079
kind: standard
trigger: "write a copy or move assignment operator"
attribution:
  - source: standard-practice
    locator: "copy and move semantics"
    upstream: ["CG C.61", "CG C.62", "CG C.64", "CG C.65"]
---

# A copy copies, a move leaves the source valid, and both handle self-assignment

After a copy, the two objects compare equal and neither shares mutable state.
After a move, the source is destructible and reassignable — empty is the usual
choice. Both assignment operators handle `x = x`.

```cpp
Toolpath& Toolpath::operator=(Toolpath&& other) noexcept {
    if (this == &other) { return *this; }
    moves_ = std::move(other.moves_);
    other.moves_.clear();              // valid, stated, empty
    return *this;
}
```

A copy that shares a buffer is an aliasing bug wearing the name of a copy. A
moved-from object left in an unspecified state cannot be safely destroyed, which
the standard library will do on your behalf. Self-assignment reaches these
operators through `std::sort` and `std::swap` whether or not any call site writes
it.
