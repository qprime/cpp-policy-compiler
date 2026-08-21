---
id: POL-0220
kind: standard
trigger: "add something to namespace std"
attribution:
  - source: standard-practice
    locator: "namespace std"
    upstream: ["CG SL.3"]
---

# Nothing is added to namespace `std` except a permitted specialization

The only legal additions are full specializations of a standard template for a
program-defined type — `std::hash`, `std::formatter`. Everything else goes in the
project's namespace.

```cpp
template <>
struct std::hash<ToolId> { std::size_t operator()(const ToolId&) const noexcept; };

namespace std { void print(const Move& move); }        // undefined behaviour
```

Adding a declaration to `std` is undefined behaviour, not merely bad style: the
standard reserves the namespace, and an implementation is free to have its own
declaration of that name. Free functions on your own types also belong in your own
namespace, where argument-dependent lookup finds them anyway.
