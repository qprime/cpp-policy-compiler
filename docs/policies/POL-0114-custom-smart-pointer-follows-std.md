---
id: POL-0114
kind: guideline
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "3. Ownership"
    upstream: ["CG R.31"]
---

# A project smart pointer follows the standard library's shape

Where a resource needs a handle the standard library does not provide, first try a
`std::unique_ptr` with a custom deleter. If a bespoke type is genuinely needed,
give it `get`, `reset`, `release`, `operator*`, `operator->`, and an explicit
`operator bool`.

```cpp
struct ClipperDeleter {
    void operator()(clipper_paths* paths) const noexcept { clipper_free(paths); }
};

using ClipperHandle = std::unique_ptr<clipper_paths, ClipperDeleter>;
```

The deleter form is a few lines and inherits move semantics, `noexcept`
correctness, and every reader's existing knowledge. A bespoke handle with different
member names forces callers to learn a second vocabulary for the same idea and
puts the exception-safety burden back on you.
