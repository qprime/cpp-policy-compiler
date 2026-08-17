---
id: POL-0125
kind: standard
attribution:
  - source: standard-practice
    locator: "copy and move operation shape"
    upstream: ["CG C.60", "CG C.61", "CG C.62", "CG C.63", "CG C.64", "CG C.65"]
---

# When copy or move is written out, it takes the standard shape

| Operation | Signature |
|-----------|-----------|
| Copy assignment | `T& operator=(const T&)`, non-`virtual` |
| Move assignment | `T& operator=(T&&) noexcept`, non-`virtual` |

A copy produces an independent object: mutating the copy must not be observable
through the original. A move leaves its source in a valid, destructible,
assignable state — empty is the usual choice, and the source is never left in a
state where the destructor is unsafe.

Both assignments are safe against self-assignment, including the move case,
which a naive release-then-take implementation gets wrong.

This is reached only when POL-0021 does not apply. Rule of zero is the default,
and a type that owns exactly one resource through a standard handle needs none
of this written out.

The shape is fixed because callers and the standard library depend on it. A
`virtual` assignment operator makes assignment through a base slice silently
(POL-0121), returning by value instead of `T&` breaks chained assignment, and a
move assignment that is not `noexcept` causes `std::vector` to copy rather than
move on reallocation — a performance change with no diagnostic.
