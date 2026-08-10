---
id: POL-0062
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions: ownership is explicit"
---

# Ownership is explicit across the FFI boundary

| Crossing | Contract |
|----------|----------|
| By value | Copies. Neither side retains a reference to the other's storage. |
| By reference | Non-owning, with the lifetime documented at the declaration. |
| Transferring ownership out of C++ | `std::unique_ptr`, or by value. Never a raw pointer. |
| Passing a mutable host object in | Valid for the duration of the call only. C++ does not retain it. |

The host language's lifetime model does not extend into C++ and C++'s does not
extend into the host. Every crossing therefore states which of the four rows it
is, at the declaration, because neither runtime can work it out.

This is POL-0014 at the one boundary where the compiler cannot help. Inside C++,
a raw pointer is non-owning by rule and a `unique_ptr` says what it means; across
the seam the type is erased by the binding, so what survives is whatever the
declaration wrote down. A retained pointer to host storage is a use-after-free
whose two halves are in different languages, which puts it beyond the reach of
every tool that would otherwise find it.
