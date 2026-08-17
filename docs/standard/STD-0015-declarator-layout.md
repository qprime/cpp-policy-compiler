---
id: STD-0015
group: layout-of-the-line
enforced_by: clang-format
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG NL.18"]
---

# The `*` and `&` bind to the type

```cpp
int* p;
const Tool& tool;
std::unique_ptr<Spindle>&& spindle;

int *p;                    // no
const Tool &tool;          // no
```

One name per declaration makes this unambiguous: `int* a, b` would declare a
pointer and an `int`, and the form that reads correctly is the one that is never
written.
