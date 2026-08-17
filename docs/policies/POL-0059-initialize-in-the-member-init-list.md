---
id: POL-0059
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: value type with invariant"
    upstream: ["CG C.13", "CG C.45", "CG C.47", "CG C.48", "CG C.49"]
---

# Members are initialized, in declaration order, not assigned

Constant initial values go in default member initializers. Values derived from
constructor arguments go in the member-init list, written in the order the members
are declared. Declare a member that another member uses before it.

```cpp
class Toolpath {
 public:
    explicit Toolpath(std::vector<Move> moves)
        : moves_(std::move(moves)), length_mm_(path_length_mm(moves_)) {}

 private:
    std::vector<Move> moves_;      // declared first: length_mm_ reads it
    double length_mm_;
    bool closed_ = false;          // constant: default member initializer
};
```

Members are initialized in declaration order regardless of the order in the
init-list, so a list written out of order reads as a lie and a member that
depends on a later one reads uninitialized storage. Assigning in the body
default-constructs first and then overwrites, which is two operations where one
was needed and impossible for a `const` member.
