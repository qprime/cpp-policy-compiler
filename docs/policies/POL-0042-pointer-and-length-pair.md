---
id: POL-0042
kind: anti-pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: pointer-and-length pair"
    upstream: ["CG I.13"]
replacement: ["POL-0041"]
---

# A pointer-and-length parameter pair

`(const T* data, std::size_t length)` puts the lifetime contract in a comment and
the bounds check on every caller. Replace it with a view.

```cpp
double path_length_mm(const Vec2* points, std::size_t count);   // no
double path_length_mm(std::span<const Vec2> points);            // instead
```

At an `extern "C"` boundary the foreign signature dictates the pair. Convert on
entry and never touch the raw pointer again.

```cpp
extern "C" int process_buffer(const Vec2* data, std::size_t length) {
    const std::span<const Vec2> path(data, length);
    // body uses path only
}
```

Nothing ties the two arguments together, so a caller who edits one and forgets
the other gets a read past the end and no diagnostic.
