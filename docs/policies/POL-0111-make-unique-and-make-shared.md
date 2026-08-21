---
id: POL-0111
kind: standard
trigger: "construct an owned heap object"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "3. Ownership"
    upstream: ["CG C.149", "CG C.150", "CG C.151", "CG R.12", "CG R.13", "CG R.22", "CG R.23"]
---

# An owned object is constructed by `make_unique` or `make_shared`, one per statement

Hand every allocation straight to the object that will own it, in the same
expression that creates it, and perform at most one allocation per statement.

```cpp
auto post = std::make_unique<GrblPost>(dialect);
auto table = std::make_shared<ToolTable>(load_tool_table(path));

process(std::unique_ptr<GrblPost>(new GrblPost(dialect)),
        std::unique_ptr<ToolTable>(new ToolTable(path)));   // no
```

In the last line the two `new` expressions and the two `unique_ptr` constructions
may interleave, so a throw from the second `new` leaks the first object — the
allocation existed for a moment with no owner. `make_shared` additionally puts the
control block and the object in one allocation.
