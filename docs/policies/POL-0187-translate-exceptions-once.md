---
id: POL-0187
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: mid-stack exception translation"
    upstream: ["CG E.17", "CG E.18"]
---

# An exception is handled where it can be acted on, and translated exactly once

Let it propagate. Catch it at the layer that can do something — retry, report to the
operator, translate at the FFI seam into the host language's mechanism — and nowhere
in between.

```cpp
// binding layer: the one translation point
PYBIND11_MODULE(proj, m) {
    py::register_exception<ToolTableError>(m, "ToolTableError");
}
```

An intermediate `try`/`catch` that only rethrows a different type adds a frame, a
type, and a place for the message to lose information, while moving the handling no
closer to anyone who can act. Where cleanup is the reason for the `catch`, an RAII
object does it without one.
