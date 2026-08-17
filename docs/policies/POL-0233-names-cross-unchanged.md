---
id: POL-0233
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# A name crosses the language boundary unchanged

`parse_layout` in Python is `parse_layout` in C++. No case conversion at the seam,
no `_impl` shim, no `parseLayout` on one side.

```cpp
PYBIND11_MODULE(proj, m) {
    m.def("parse_layout", &proj::parse_layout);
}
```

```python
from proj import parse_layout          # the same name, spelled the same way
```

A renaming seam means every cross-language search returns half its hits and every
stack trace changes vocabulary at the boundary. This is the reason the case table is
mandated machine-wide rather than chosen per project: identical names across the
boundary are only achievable if both languages already agree on case.
