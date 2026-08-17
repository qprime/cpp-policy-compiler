---
id: POL-0088
kind: pattern
attribution:
  - source: standard-practice
    locator: "container requirements"
    upstream: ["CG C.100", "CG C.101", "CG C.102", "CG C.103", "CG C.104"]
---

# A container written here follows the standard library's shape

Give it value semantics, move operations, an initializer-list constructor, a
default constructor that produces an empty container, and the standard member
names — `begin`, `end`, `size`, `empty`, `value_type`.

```cpp
class MoveList {
 public:
    using value_type = Move;

    MoveList() = default;
    MoveList(std::initializer_list<Move> moves) : moves_(moves) {}

    auto begin() const { return moves_.begin(); }
    auto end() const { return moves_.end(); }
    std::size_t size() const { return moves_.size(); }
    bool empty() const { return moves_.empty(); }

 private:
    std::vector<Move> moves_;
};
```

Matching the shape is what makes the type work with range-`for`, the algorithms,
and every generic function already written. A container with `count()` instead of
`size()` needs a wrapper at every one of those sites.

Before writing one, check that composing `std::vector` does not already do the
job.
