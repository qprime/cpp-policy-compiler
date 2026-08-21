---
id: POL-0183
kind: pattern
trigger: "decide how an operation reports that it failed"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: failure mechanism"
    upstream: ["CG E.1", "CG E.4"]
---

# Pick the failure mechanism from what the caller needs

| Mode | Use when |
|------|----------|
| Standard optional | Absence is the only failure mode; there is nothing to explain |
| Result type (`std::expected` on C++23, a project result type earlier) | Failure carries information the caller must act on |
| Exception | Genuinely exceptional: allocation failure, invariant violation, unrecoverable corruption |
| `assert` | "Cannot happen" — upstream validation already guarantees it |
| Silent partial output | **Never** |

```cpp
std::optional<Tool> find_tool(const ToolTable& table, int slot);
Result<Job, ParseError> parse_job(std::string_view text);
ConvexPolygon::ConvexPolygon(Polygon points);   // throws: the invariant is the point
```

Decide this per module before writing the functions, and decide it around the
invariants: a failure that means *this object cannot exist* belongs in a
constructor, and one that means *this input was wrong* belongs in the return type.
Mixing mechanisms inside one module makes every caller check two ways.

Failures also get less fatal outward: a parser is strict, a module API returns a
result, an orchestrator tolerates per-item failure, and the FFI boundary translates.
