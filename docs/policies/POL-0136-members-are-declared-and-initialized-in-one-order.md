---
id: POL-0136
kind: standard
attribution:
  - source: standard-practice
    locator: "member declaration and initialization order"
    upstream: ["CG C.13", "CG C.47", "CG C.48", "CG Type.6"]
---

# Members initialize in declaration order, and every member is initialized

```cpp
// Never. count_ is initialized first, from an uninitialized values_.
class Histogram {
 public:
    explicit Histogram(std::vector<int> values)
        : count_{values_.size()}, values_{std::move(values)} {}
 private:
    std::size_t count_;
    std::vector<int> values_;
};

// Right. Declaration order is initialization order, and one default is stated once.
class Histogram {
 public:
    explicit Histogram(std::vector<int> values)
        : values_{std::move(values)}, count_{values_.size()} {}
 private:
    std::vector<int> values_;
    std::size_t count_{0};
};
```

A member that depends on another is declared after it. A member with the same
initial value in every constructor uses a default member initializer, stated
once at the declaration rather than repeated in each constructor list.

Members initialize in declaration order regardless of the order written in the
initializer list, so a list that disagrees with the declarations reads as one
sequence and executes as another. Reading a member before its initializer has
run is undefined behaviour, and `-Wreorder` under POL-0089 is what makes the
mismatch a build error rather than a silent one.

Leaving a member uninitialized is the class-scope form of POL-0096, with the
same consequence and less visibility: the window is every constructor that
forgets it, not one declaration a reader can see.
