---
id: STD-0011
group: names
enforced_by: review
review_trigger: "a function name obscures its return or failure contract"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Naming Vocabulary"
---

# A name prefix states the return contract

| Pattern | Returns |
|---------|---------|
| `is_*` / `has_*` | `bool` |
| `try_*` / `try_from` | Optional or result — never throws |
| `get_*` | An accessor that cannot fail; the precondition is the caller's |
| `find_*` | Optional or iterator |
| `make_*` | Constructs a value |

```cpp
bool is_closed(const Polygon& poly);
static std::optional<ConvexPolygon> try_from(Polygon points);
const Tool* find_tool(const ToolTable& table, int slot);
std::unique_ptr<PostProcessor> make_post(GrblDialect dialect);
```

A `try_` that throws or a `find_` that returns a bare value breaks the contract the
prefix advertised, which is worse than having no convention at all.
