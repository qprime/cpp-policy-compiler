---
id: POL-0120
kind: standard
attribution:
  - source: standard-practice
    locator: "polymorphic class shape"
    upstream: ["CG C.67", "CG C.127", "CG C.130", "CG C.133", "CG NR.7"]
---

# A class with a virtual function states its destructor and suppresses copying

```cpp
class Exporter {
 public:
    virtual ~Exporter() = default;
    Exporter(const Exporter&) = delete;
    Exporter& operator=(const Exporter&) = delete;
    Exporter(Exporter&&) = delete;
    Exporter& operator=(Exporter&&) = delete;

    virtual void write(std::span<const Move> moves) = 0;

 protected:
    Exporter() = default;
};
```

The destructor is public and `virtual` where the base is deleted through, and
protected and non-`virtual` where it is not. Copy and move are deleted, because
copying a base subobject out of a derived object is the slicing POL-0121
forbids; a hierarchy that needs copying provides a `virtual clone` returning
`std::unique_ptr`.

Data members are `private`. `protected` data is an interface with no
invariant — every derived class can break what the base established, and the
base has no way to state what it required.

Deleting through a base with a non-`virtual` destructor is undefined behaviour,
and it is undefined silently: the derived destructor does not run, so the
program leaks or corrupts rather than crashing where the mistake is. Stating
the destructor either way makes the decision visible at the point a reader asks
whether this type is meant to be deleted polymorphically.

This applies only once POL-0037 has established that a hierarchy is right at
all. Variation among a fixed set of alternatives is `std::variant` (POL-0044).
