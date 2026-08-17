---
id: POL-0235
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
---

# Absence crosses as absence; NaN never crosses

`std::optional<T>` maps to `Optional[T]` and `std::nullopt` maps to `None`. An empty
collection means an empty collection, never a failure. A NaN reaching the seam is a
defect to investigate, not a value to translate.

```cpp
m.def("find_tool", [](const ToolTable& table, int slot) -> std::optional<Tool> {
    return find_tool(table, slot);        // nullopt becomes None
});
```

Each language already has a way to say *nothing here*, so re-encoding absence into a
sentinel at the seam invents a third convention both sides then have to know. NaN is
the worst of those sentinels: it means *invalid number*, so letting it cross makes a
real arithmetic bug indistinguishable from an intentional absence, on the far side of
the boundary from where it happened.
