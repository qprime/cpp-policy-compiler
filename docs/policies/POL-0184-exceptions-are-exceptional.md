---
id: POL-0184
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Divergences: [CG E.2], [CG I.10]"
    upstream: ["CG E.2", "CG E.3", "CG I.10"]
---

# Exceptions are for genuinely exceptional conditions, never for control flow

Throw on allocation failure, invariant violation, and unrecoverable corruption. A
routine fallible operation — a lookup that misses, a parse that fails — returns
`std::optional` or a result type.

```cpp
std::optional<Tool> find_tool(const ToolTable& table, int slot);   // routine miss

Tool find_tool(const ToolTable& table, int slot);   // throws when absent: no
```

The Core Guidelines make exceptions the general failure mechanism; this corpus does
not, because exceptions are forbidden in real-time loops and never cross the FFI
un-translated. Neither constraint is assumed upstream.

An exception used as a branch also costs its throw path far more than a return and
hides the branch from every reader of the signature.
