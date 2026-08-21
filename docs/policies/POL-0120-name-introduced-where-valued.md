---
id: POL-0120
kind: standard
trigger: "declare a variable"
attribution:
  - source: standard-practice
    locator: "declaration scope"
    upstream: ["CG ES.5", "CG ES.6", "CG ES.21", "CG ES.22"]
---

# A name is introduced where it gets its value, in the smallest scope that needs it

Declare and initialize in one statement, at the point of first use. Put loop and
condition variables in the `for` initializer or the `if` initializer.

```cpp
for (std::size_t i = 0; i < rings.size(); ++i) { ... }

if (const auto found = find_tool(table, slot); found != nullptr) { ... }

double area_mm2;                    // no: declared here, valued 30 lines later
```

A name alive before it has a value is a name that can be read before it has one,
and the compiler cannot always tell. Narrowing the scope also shortens the range
of code a reader must hold in mind to know what the name currently means.
