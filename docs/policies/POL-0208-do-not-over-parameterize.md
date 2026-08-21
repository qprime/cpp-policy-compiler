---
id: POL-0208
kind: guideline
trigger: "write a member that does not use its class template's parameter"
attribution:
  - source: standard-practice
    locator: "template instantiation cost"
    upstream: ["CG T.61", "CG T.62"]
---

# A member that does not use a template parameter does not depend on it

Move members that do not mention the parameter into a non-template base or a free
function, so they are compiled once rather than per instantiation.

```cpp
class PathBase {
 protected:
    bool closed_ = false;
    std::size_t revision_ = 0;
    void bump_revision() { ++revision_; }       // one copy, ever
};

template <class T>
class Path : public PathBase {
    std::vector<Vec2Of<T>> points_;
};
```

Each instantiation gets its own copy of every member, including the ones that are
identical across all of them, and each copy is separate code for the linker to
merge and the reader to step through. Over-parameterized nested types also make
`Path<float>::iterator` and `Path<double>::iterator` unrelated when they need not be.
