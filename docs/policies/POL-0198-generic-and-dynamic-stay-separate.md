---
id: POL-0198
kind: guideline
trigger: "erase a type, or mix a generic layer with a polymorphic one"
attribution:
  - source: standard-practice
    locator: "generic and object-oriented styles"
    upstream: ["CG T.5", "CG T.49"]
---

# Keep the generic layer and the polymorphic layer distinct, and avoid type erasure

Use templates for compile-time variation and an interface for run-time variation.
Do not build a type-erasing wrapper to hide one behind the other unless the
alternative is worse.

```cpp
template <class Emitter>
void stream(const Paths& paths, Emitter& emitter);     // compile-time variation

void stream(const Paths& paths, PostProcessor& post);  // run-time variation
```

Type erasure buys a uniform signature and costs an allocation, an indirection, and
the loss of every constraint the concept was carrying. When both layers exist in one
type, neither the compiler nor the reader can tell which variation a given call
resolves through.
