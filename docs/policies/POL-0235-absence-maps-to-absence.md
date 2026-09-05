---
id: POL-0235
kind: standard
trigger: "send an absent or NaN value across the boundary"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# Absence crosses as absence; NaN is never an absence sentinel

`std::optional<T>` maps to `Optional[T]` and `std::nullopt` maps to `None`. An empty
collection means an empty collection, never a failure. Do not translate absence to
NaN. A NaN may cross only when it is a legitimate value in the documented numeric
domain; otherwise reject it at the boundary as invalid input or arithmetic output.

```cpp
m.def("find_tool", [](const ToolTable& table, int slot) -> std::optional<Tool> {
    return find_tool(table, slot);        // nullopt becomes None
});
```

Each language already has a way to say *nothing here*, so re-encoding absence into a
sentinel at the seam invents a third convention both sides then have to know. NaN is
an especially poor sentinel because it makes an arithmetic result indistinguishable
from intentional absence, on the far side of where it happened.
