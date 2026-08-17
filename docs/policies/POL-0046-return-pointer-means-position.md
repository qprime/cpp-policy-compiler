---
id: POL-0046
kind: guideline
attribution:
  - source: standard-practice
    locator: "returning positions"
    upstream: ["CG F.42"]
---

# A returned raw pointer means a position, never a transfer

Return `T*` to say *here is the one you asked about, or nothing*. The caller
neither deletes it nor outlives the container that holds it.

```cpp
const Tool* find_tool(const ToolTable& table, int slot);   // position, may be null
std::unique_ptr<Tool> make_tool(const ToolSpec& spec);     // transfer, says so
```

Callers read a returned pointer as *non-owning and valid while the source is* —
so returning an owning one leaks by default. When absence is the only reason for
the pointer, `std::optional<T>` says it without the lifetime question.
