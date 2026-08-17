---
id: POL-0028
kind: guideline
attribution:
  - source: standard-practice
    locator: "encapsulating unsafe code"
    upstream: ["CG I.30"]
---

# A necessary rule violation is confined to one named place

When correctness requires something the rules forbid — a cast through a foreign
API, manual lifetime management, a platform trick — put it in one small function
or type, name it for what it does, and say in a comment which rule it breaks and
why.

```cpp
namespace detail {

// Owning raw pointer: the C API allocates and requires its own free.
struct ClipperDeleter {
    void operator()(clipper_paths* paths) const noexcept { clipper_free(paths); }
};

using ClipperHandle = std::unique_ptr<clipper_paths, ClipperDeleter>;

}  // namespace detail
```

Contained, the violation is one reviewable site with a stated reason. Spread, it
becomes the local style, and the next author cannot tell a necessary exception
from a habit.
