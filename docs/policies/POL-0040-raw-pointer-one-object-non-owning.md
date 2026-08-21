---
id: POL-0040
kind: standard
trigger: "declare a raw pointer"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "3. Ownership"
    upstream: ["CG F.22", "CG R.2", "CG R.3", "CG R.4"]
---

# A raw pointer denotes one object and never owns it

`T*` in an interface means: exactly one object, someone else owns it, and null
is a value the function handles. Not an array, not a range, not a transfer.

```cpp
const Tool* active_tool(const ToolTable& table);      // one object, may be absent
void render(const Move* moves, std::size_t count);    // no — a range in disguise
```

Once a raw pointer can mean *array* or *owner*, no reader can tell which one a
given signature intends, and the type system stops helping. Holding the meaning
to one object per pointer is what makes the ownership question answerable from
the declaration.
