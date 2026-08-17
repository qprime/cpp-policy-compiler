---
id: STD-0003
group: files-and-layout
enforced_by: review
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: module boundary"
    upstream: ["CG SF.20"]
---

# Headers live under `include/<project>/<layer>/`, and namespaces nest by layer

| Thing | Shape |
|-------|-------|
| Public header | `include/<project>/<layer>/<file>.hpp` |
| Source | `<layer>/<file>.cpp` |
| Namespace | `<project>::<layer>`, `snake_case` |
| Include path | Always from the project root: `"proj/algo/plan_2d.hpp"` |

```cpp
// include/proj/algo/plan_2d.hpp
namespace proj::algo {

Paths plan_pocket(const PlanarFace& face, const Tool& tool,
                  const PocketParams& params);

}  // namespace proj::algo
```

The namespace path and the include path match, so a name in a diagnostic tells you
which file to open.
