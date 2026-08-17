---
id: POL-0017
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: when a thing becomes a type"
    upstream: ["CG I.4"]
---

# An interface takes the type that carries the meaning

Work down the list; stop at the first match.

| Question | If yes |
|----------|--------|
| Is there a combination of values that must never exist? | A `class` with a validating constructor |
| Is there a structural precondition other code wants to assume? | A wrapper type |
| Is it a fixed set of alternatives? | `enum class`, or a variant if the alternatives carry payloads |
| Do several values always travel together? | A params struct or an aggregate |
| None of the above | A primitive with a unit-suffixed name — the common case |

```cpp
Paths plan_pocket(const ConvexPolygon& face, const Tool& tool, double safe_z_mm);
Paths plan_pocket(const std::vector<double>& face, double d, double r, double z);
```

The second signature admits every wrong call the first refuses. Precision at the
interface is what lets the body stop checking.
