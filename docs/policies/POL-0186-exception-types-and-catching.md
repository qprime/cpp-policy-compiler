---
id: POL-0186
kind: standard
trigger: "throw or catch"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: failure mechanism"
    upstream: ["CG E.14", "CG E.15", "CG E.31"]
---

# Throw a purpose-designed type by value; catch by `const&`, most-derived first

Define an exception type for the failure, deriving from `std::exception` or a
project base. Never throw a built-in or a `std::string`. Order `catch` clauses from
most derived to least.

```cpp
class ToolTableError : public std::runtime_error {
 public:
    using std::runtime_error::runtime_error;
};

throw ToolTableError("ToolTable: slot must be in [1, 24], got 0");

try {
    load();
} catch (const ToolTableError& e) {      // derived first
    ...
} catch (const std::exception& e) {      // base last
    ...
}
```

A thrown `int` or string carries no type for a handler to select on, so every
handler catches everything or nothing. Catching by value slices a derived exception
down to the base. A base clause written first catches derived exceptions too, making
the later clauses dead code — some compilers warn, and the ones that do not leave a
handler that never runs.
