---
id: POL-0237
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# Ownership across the boundary is by value or by a stated non-owning reference

A by-value crossing copies. A by-reference crossing is non-owning with a documented
lifetime. C++ does not hand raw pointers to the host, and the host does not pass
mutable objects expecting C++ to retain them past the call.

```cpp
m.def("plan_pocket", [](const PocketParams& params) {
    return plan_pocket(params);           // returns by value; Python owns the result
});

m.def("adopt_table", [](ToolTable* table) { ... });   // no: whose delete is it?
```

Neither language's lifetime machinery is visible to the other, so a raw pointer
crossing has an owner that only a comment records. The reference-counting host will
free what it thinks it owns, or never free what it thinks it does not — and both
outcomes surface a long way from the seam.
