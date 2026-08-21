---
id: POL-0036
kind: standard
trigger: "choose how a parameter is passed"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: how to pass a parameter"
    upstream: ["CG F.15", "CG F.16", "CG F.17", "CG F.60"]
---

# Parameter passing is conventional, never clever

The table is the whole decision.

| Pass by | When |
|---------|------|
| Value | Small and cheap to copy (`double`, `Vec2`, an enum); or you modify your own copy; or you move from it |
| `const T&` | Larger types you only read |
| `T&` | In-out. Rare — prefer returning a value |
| `T*` | Null is a meaningful value |
| `T&&` | You will move from it and the caller knows |
| Sequence view | A read-only or write-through sequence |

```cpp
double area_mm2(const ConvexPolygon& poly);          // read a large type
Vec2 midpoint(Vec2 a, Vec2 b);                       // cheap values
void append_to(Path& path, const Move& move);        // in-out, deliberate
const Tool* active_tool(const ToolTable& table);     // absence is meaningful
```

Every departure from the table is a question the reader has to answer before
they can read the body. There is nothing to gain by being novel here, and the
conventions are what let a signature be understood without reading the
implementation.
