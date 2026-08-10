---
id: POL-0086
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Naming vocabulary: pattern table"
---

# A name prefix states the return contract

| Pattern | Returns |
|---------|---------|
| `is_*` / `has_*` | `bool` |
| `try_*` / `try_from` | An optional or a result. Never throws |
| `get_*` | An accessor that cannot fail; the precondition is the caller's |
| `find_*` | An optional or an iterator |
| `make_*` | Constructs a value |

The contract runs both ways. A function named `try_*` that throws is a defect,
and so is a fallible operation named `get_*`.

`try_from` is the non-throwing companion to a validating constructor
(POL-0022) and to a wrapper type's conversion (POL-0027). Where one exists, this
is its name.

The prefix is the part of a signature a reader sees before the return type, and
at a call site it is often the only part they see. A `find_` that returns an
optional and a `get_` that cannot fail need different handling at every call, so
encoding the difference in the prefix means the handling is chosen while writing
rather than after a compile error. The rule earns most where the return type is
elided (POL-0050): with `auto` on the left, the prefix is all the reader has.
