---
id: POL-0244
kind: standard
trigger: "add a test file, or a second test for one behaviour"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# One test per behaviour; check what exists before adding a file

Before writing a test, search for one covering the same behaviour over the same
input. Two tests asserting the same thing is a defect, not extra safety.

```cpp
TEST_CASE("Tool rejects a zero diameter") { ... }
TEST_CASE("constructing a tool with diameter 0 throws") { ... }   // the same test
```

Duplicates both fail together, so the second one adds nothing to the report and
doubles the work of every future change to that behaviour. They also make the suite
look like it covers more than it does, which is how a genuine gap stays hidden.
