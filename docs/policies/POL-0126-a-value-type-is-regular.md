---
id: POL-0126
kind: standard
attribution:
  - source: standard-practice
    locator: "regular value types"
    upstream: ["CG C.11", "CG C.12", "CG C.43", "CG C.44", "CG C.134"]
---

# A value type behaves like `int`

```cpp
class Millis {
 public:
    Millis() = default;
    explicit constexpr Millis(double count) : count_{count} {}
    constexpr double count() const { return count_; }
 private:
    double count_{0.0};
};
```

Copyable, movable, comparable, default-constructible to a meaningful empty or
zero, and free of surprises when placed in a container. The default constructor
is simple and does not throw.

No data member is `const` or a reference on a copyable or movable type. Either
one deletes assignment silently, so the type stops being assignable and every
container operation that needs assignment stops compiling, with an error that
points at the container rather than at the member.

Every non-`const` data member is `private`. Mixed access levels mean part of the
representation is an invariant and part is not, and no reader can tell which
without checking each one. A type whose members are genuinely all public and
constraint-free is an aggregate `struct` (POL-0042), not a class with some
members exposed.

Regularity is what lets a type be used without being studied. A value that
copies, compares, and sorts the way `int` does needs no documentation to be put
in a `std::vector` or a `std::map`, and every deviation is a special case
someone has to learn before they can use it (POL-0004).
