---
id: POL-0078
kind: standard
attribution:
  - source: standard-practice
    locator: "assignment operator conventions"
    upstream: ["CG C.60", "CG C.63", "CG F.47"]
---

# Assignment is non-`virtual`, takes `const&` or `&&`, and returns `T&`

```cpp
class Toolpath {
 public:
    Toolpath& operator=(const Toolpath& other);
    Toolpath& operator=(Toolpath&& other) noexcept;
};
```

This is the shape every standard container, algorithm, and generic function
expects. Returning `void` breaks chained assignment and some generic code;
returning by value copies for nothing; making it `virtual` invites assigning a
derived object through a base reference, which slices.
