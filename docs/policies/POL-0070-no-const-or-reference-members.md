---
id: POL-0070
kind: standard
trigger: "declare a const or reference data member"
attribution:
  - source: standard-practice
    locator: "assignable members"
    upstream: ["CG C.12"]
---

# A copyable or movable type has no `const` and no reference members

Store values and keep the member non-`const`; the accessor and the class's
interface are what make it read-only from outside.

```cpp
class Cut {
 public:
    const Tool& tool() const { return tool_; }

 private:
    Tool tool_;                  // value; assignment works
    const Tool& tool_;           // no: kills copy assignment and move assignment
};
```

A `const` or reference member cannot be reassigned, so the compiler deletes copy
assignment and move assignment. The type then fails to work in a `std::vector`,
in `std::sort`, or anywhere assignment is required — usually discovered a long way
from the declaration that caused it.
