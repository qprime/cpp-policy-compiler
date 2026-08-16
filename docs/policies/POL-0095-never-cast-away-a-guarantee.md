---
id: POL-0095
kind: anti-pattern
replacement: [POL-0094]
attribution:
  - source: standard-practice
    locator: "casts, undefined behaviour"
    upstream: ["CG ES.50", "CG Type.1"]
---

# Never cast away const, and never reinterpret an object's bytes through a pointer

```cpp
// Never. If the referent is genuinely const, the write is undefined behaviour.
void touch(const Config& cfg) {
    const_cast<Config&>(cfg).retries = 3;
}

// Never. Type-punning through a pointer cast breaks strict aliasing.
const float bits = *reinterpret_cast<const float*>(&raw_word);
```

If a function needs to modify what it was given, it takes a non-const
reference and says so in its signature. If bytes genuinely need
reinterpreting, use `std::bit_cast` on C++20 and `std::memcpy` before it; both
are defined and both optimize to the same instruction.

`const_cast` compiles identically whether or not the original object was
declared const, so the undefined case and the merely-ugly case are
indistinguishable at the point the cast is written. The alias violation is
worse: it produces a program that behaves correctly at low optimization levels
and changes behaviour when the optimizer is turned up, which places the failure
in the build configuration rather than in the line that caused it (POL-0019).
