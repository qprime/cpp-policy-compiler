---
id: POL-0205
kind: guideline
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "9. Generic code"
    upstream: ["CG T.44"]
---

# Where class template arguments should be deduced, provide a `make_*` function

Rely on deduction guides or CTAD where they read clearly. Where they do not, write a
factory function whose arguments deduce.

```cpp
template <class T>
Span<T> make_span(std::vector<T>& values) { return Span<T>{values.data(), values.size()}; }

auto path = make_span(points);          // deduced
Span<Vec2> path{points.data(), points.size()};   // spelled out at every call
```

The factory turns an explicit type argument into a deduced one, which removes a
place for the argument and the container's element type to disagree. It is also the
only route on standards without CTAD.
