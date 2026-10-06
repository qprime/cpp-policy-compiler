---
id: POL-0237
kind: standard
trigger: "pass ownership across the boundary"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# Ownership across the boundary is by value or by a stated non-owning reference

A by-value crossing gives the receiver its own value through conversion, copy,
or move according to the binding contract. A borrowed crossing has an explicit
lifetime and does not transfer deletion responsibility. Do not transfer ownership
through an undocumented raw pointer, or retain a caller's borrowed object past
the lifetime guaranteed by the interface. An owning handle may cross when its
release operation and allocator pairing are explicit.

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

Binding libraries can keep an owner alive or adopt an object deliberately. State
that policy at the binding rather than assuming C++ reference syntax establishes
it. For example, pybind11 distinguishes copy, move, reference, reference-internal,
and ownership-transfer return policies; its default raw-pointer return policy can
take ownership. Check the actual policy before exposing a pointer or reference.
