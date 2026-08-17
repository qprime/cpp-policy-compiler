---
id: POL-0121
kind: anti-pattern
replacement: [POL-0120]
attribution:
  - source: standard-practice
    locator: "polymorphic class shape, slicing"
    upstream: ["CG ES.63", "CG C.145", "CG C.152", "CG T.81"]
---

# Never copy a polymorphic object by value, and never index one through a base pointer

```cpp
// Never. Copies the Exporter subobject; the derived half is discarded.
void emit(Exporter e);

// Never. Base and derived have different sizes; the arithmetic is wrong.
GcodeExporter items[4];
Exporter* p = items;
p[2].write(moves);

// Right. Access through a reference or a pointer, hold ownership as unique_ptr.
void emit(const Exporter& e);
std::vector<std::unique_ptr<Exporter>> exporters;
```

A container of polymorphic objects holds `std::unique_ptr` (POL-0014), never
values, and never a raw array.

Slicing compiles without a diagnostic and produces an object of the base type
holding the base's data, so the virtual call dispatches to the base
implementation and the derived behaviour is simply absent. Nothing reports it;
the program runs and does the wrong thing, which is the failure POL-0002 ranks
worst.

Array indexing through a base pointer is the same defect in pointer arithmetic:
the subscript scales by the base's size while the objects are the derived size,
so every element past the first addresses the middle of an object.
