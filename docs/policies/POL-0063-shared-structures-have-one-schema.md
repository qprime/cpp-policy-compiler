---
id: POL-0063
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions: the IR is the contract"
---

# A structure shared across the boundary has one schema and one source of truth

Any structure both sides read or write — an intermediate representation, a
parsed model, a result payload — is defined once. The other side derives from
that definition rather than restating it.

A schema change is versioned and moves everything together, in one change:

1. define the new form in the schema
2. expose it across the FFI
3. document it
4. regenerate the goldens (POL-0071)

Adding an alternative to a shared structure follows the same four steps in the
same order. A definition that has moved without its goldens is a change nobody
can review, because the diff that would have shown its effect was not produced.

Two definitions of one structure agree on the day they are written and are edited
independently after. The disagreement does not fail to compile, because each side
compiles against its own copy; it appears as a field silently dropped or misread
at the seam, at runtime, on the inputs that exercise the new field. One
definition makes the mismatch a build failure, which is the only form of it that
is found before the data is wrong.
