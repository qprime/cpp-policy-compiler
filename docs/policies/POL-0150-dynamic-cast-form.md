---
id: POL-0150
kind: standard
attribution:
  - source: standard-practice
    locator: "dynamic_cast"
    upstream: ["CG C.146", "CG C.147", "CG C.148", "CG Type.2"]
---

# Navigating a hierarchy uses `dynamic_cast`, and its form states whether failure is expected

```cpp
// Never. static_cast down is unchecked: wrong type, undefined behaviour, no diagnostic.
auto& gcode = static_cast<GcodeExporter&>(exporter);

// Right. Failure is a defect here, so the reference form throws.
auto& gcode = dynamic_cast<GcodeExporter&>(exporter);

// Right. Failure is an expected outcome, so the pointer form returns null.
if (auto* gcode = dynamic_cast<GcodeExporter*>(&exporter)) { gcode->emit_header(); }
```

The reference form where not finding the type is a programming error, since it
throws `std::bad_cast` and cannot be ignored. The pointer form where absence is
a normal case, since it yields `nullptr` and the check is the branch.

`static_cast` to a derived type performs no check at all. If the object is not
that type the program has undefined behaviour, and it usually proceeds — reading
members at offsets that belong to something else.

Reaching for either is a signal first. A `dynamic_cast` in ordinary code usually
means the operation belongs on the interface as a virtual function (POL-0037),
or that the set of alternatives is closed and should have been a `std::variant`
(POL-0044). The cast is for the case where the hierarchy is genuinely open and
navigation is genuinely unavoidable.
