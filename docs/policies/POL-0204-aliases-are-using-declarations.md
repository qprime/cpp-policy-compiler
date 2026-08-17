---
id: POL-0204
kind: standard
attribution:
  - source: standard-practice
    locator: "type aliases"
    upstream: ["CG T.42", "CG T.43"]
---

# An alias is a `using` declaration, and it hides a detail worth hiding

Never `typedef`. Introduce an alias to shorten a type the reader would otherwise
reassemble, or to name a project-level choice in one place.

```cpp
using ClipperHandle = std::unique_ptr<clipper_paths, ClipperDeleter>;

template <class T>
using PathOf = std::vector<Vec2Of<T>>;

typedef std::unique_ptr<clipper_paths, ClipperDeleter> ClipperHandle;   // no
```

`using` reads left to right, works for alias templates, and `typedef` does neither —
there is no template `typedef`. An alias that merely renames a short type adds a
name the reader has to resolve and hides nothing.
