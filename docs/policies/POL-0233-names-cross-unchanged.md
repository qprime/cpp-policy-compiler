---
id: POL-0233
kind: standard
trigger: "rename something as it crosses the language boundary"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# Cross-language names are identical unless one explicit boundary mapping improves the public API

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

Prefer identical names because they preserve searchability and stack-trace
vocabulary. When the foreign language's established public convention requires a
different spelling, declare that transformation once in the binding layer; do not
scatter `_impl` aliases or ad hoc renames through either codebase.
