---
id: POL-0032
kind: standard
trigger: "write noexcept"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: blanket noexcept"
    upstream: ["CG F.6", "CG E.12"]
---

# `noexcept` is a claim, written only where it is true and matters

Write it on move operations, `swap`, destructors, hash functions, and pure
arithmetic over built-ins. Leave it off anything that allocates, formats,
or calls code you do not control.

```cpp
Toolpath(Toolpath&&) noexcept;                          // true and load-bearing
std::string format_move(const Move& move) noexcept;     // allocates; the claim is false
```

If the claim is false the program calls `std::terminate` — the exception is not
propagated, it is fatal. "It is free" is wrong: on a move operation `noexcept` is
what lets `std::vector` reallocate by moving, and everywhere else it is a promise
with a crash attached.
