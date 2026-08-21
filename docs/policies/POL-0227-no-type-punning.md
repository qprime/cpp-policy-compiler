---
id: POL-0227
kind: standard
trigger: "reinterpret an object's bytes"
attribution:
  - source: standard-practice
    locator: "type punning"
    upstream: ["CG C.183"]
---

# Reinterpreting an object's bytes goes through `std::bit_cast` or a byte copy, never a `union`

Read the bytes out with `std::bit_cast` where the types are the same size and
trivially copyable, or `std::memcpy` into the target type. Never write one union
member and read another.

```cpp
const std::uint64_t bits = std::bit_cast<std::uint64_t>(position_mm);

union Pun { double d; std::uint64_t u; };
Pun pun; pun.d = position_mm; use(pun.u);        // undefined behaviour
```

Only the most recently written union member is alive, so reading a different one is
undefined behaviour — and it is one of the cases optimizers act on, so the value
read can differ between builds. `std::bit_cast` and `memcpy` are the two forms the
standard defines for this, and both are compiled to the same nothing.
