---
id: STD-0002
group: files-and-layout
enforced_by: review
attribution:
  - source: cpp-convention/conventions.md
    locator: "Naming"
---

# File names are `snake_case`

```
plan_2d.cpp          tool_table.hpp          convex_polygon.hpp
Plan2D.cpp           toolTable.hpp                                 // no
```

A file holding one type is named for that type, converted to `snake_case`:
`ConvexPolygon` lives in `convex_polygon.hpp`.
