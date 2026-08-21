---
id: POL-0049
kind: standard
trigger: "return an rvalue reference, or move a local on the way out"
attribution:
  - source: standard-practice
    locator: "return value optimization"
    upstream: ["CG F.45", "CG F.48"]
---

# Do not return `T&&`, and do not `return std::move(local)`

Return by value and let the compiler elide the copy. The only `std::move` in a
return statement is on a member or a parameter, never on a local.

```cpp
Toolpath build() {
    Toolpath path = assemble();
    return path;                    // elided; nothing to move
}

Toolpath build() {
    Toolpath path = assemble();
    return std::move(path);         // defeats elision, and warns
}
```

`return std::move(local)` turns a free elision into a move, and returning `T&&`
hands back a reference to storage the frame is about to release. Both are
pessimizations dressed as optimizations.
