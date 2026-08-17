---
id: POL-0039
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: how to pass a parameter"
    upstream: ["CG F.19"]
---

# A forwarding parameter takes `TP&&` and is only ever forwarded

`TP&&` on a deduced template parameter is a forwarding reference, not an rvalue
reference. Pass it on with `std::forward<TP>` and do nothing else with it.

```cpp
template <class... Args>
Tool& emplace_tool(ToolTable& table, Args&&... args) {
    return table.emplace_back(std::forward<Args>(args)...);
}
```

`std::move` on a forwarding reference steals from an lvalue the caller still
owns. Reading the parameter after forwarding reads a moved-from object. Forward
once, at the end, and the category the caller supplied is the category the
callee sees.
