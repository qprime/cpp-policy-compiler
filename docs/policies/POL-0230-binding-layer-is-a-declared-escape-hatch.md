---
id: POL-0230
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
    upstream: ["CG P.7"]
---

# The binding layer is the one place boundary ceremony is correct

Everywhere else, validate at the outer boundary and trust inward. The binding layer
is the declared exception: it converts, validates, and translates at the seam, and
it is permitted the boilerplate that implies. Say so in its header.

```cpp
// bindings/proj_py.cpp
// This layer is the declared escape hatch from validate-at-the-boundary. It
// converts, validates, and translates on the way in and on the way out. The
// ceremony below is correct here and nowhere else.

PYBIND11_MODULE(proj, m) {
    m.def("plan_pocket", [](const py::dict& params) {
        return plan_pocket(to_pocket_params(params));   // converts and validates
    });
}
```

Without the declaration, the next reader sees defensive code and either copies the
style inward or deletes it as redundant. Naming the layer as an exception is what
keeps the general rule intact while letting this one file do what it must.
