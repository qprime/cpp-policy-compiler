---
id: POL-0077
kind: guideline
attribution:
  - source: standard-practice
    locator: "constructor delegation"
    upstream: ["CG C.51", "CG C.52"]
---

# Shared constructor work is delegated, not duplicated

When several constructors do the same setup, delegate to the one that does the
work. When a derived class adds no state, inherit the base constructors instead of
retyping them.

```cpp
class Tool {
 public:
    Tool(double diameter_mm, double rpm);
    explicit Tool(double diameter_mm) : Tool(diameter_mm, 0.0) {}
};

class GrblPost final : public PostProcessor {
 public:
    using PostProcessor::PostProcessor;    // adds no state of its own
};
```

Duplicated validation drifts: the fix goes into one constructor and the other
keeps accepting the bad input. Delegation makes the invariant live in exactly one
body.

Inheriting constructors are only correct while the derived class has no members of
its own to initialize — adding one makes them a bug.
