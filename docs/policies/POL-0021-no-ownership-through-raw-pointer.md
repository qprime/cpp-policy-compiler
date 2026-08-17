---
id: POL-0021
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: ownership decision"
    upstream: ["CG I.11"]
---

# Ownership never transfers through a raw pointer or reference

A `T*` or `T&` crossing an interface is non-owning, in both directions. A
function that takes ownership takes `std::unique_ptr<T>` by value; a function
that hands ownership back returns one.

```cpp
void adopt(std::unique_ptr<Spindle> spindle);   // takes ownership, says so
void adopt(Spindle* spindle);                  // maybe deletes it; nobody knows
std::unique_ptr<Spindle> make_spindle(const SpindleConfig& config);
```

With the raw pointer the caller cannot tell whether to delete, and the callee
cannot tell whether it may. Every such pair is either a leak or a double free,
decided by convention rather than by the type.
