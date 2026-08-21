---
id: POL-0076
kind: guideline
trigger: "construct an object that needs a virtual step to finish"
attribution:
  - source: standard-practice
    locator: "two-phase construction"
    upstream: ["CG C.50"]
---

# Where construction needs virtual behaviour, use a factory function

Finish the object, then call the virtual step from a factory that returns it.

```cpp
std::unique_ptr<PostProcessor> make_post(GrblDialect dialect) {
    auto post = std::make_unique<GrblPost>(dialect);
    post->load_macros();          // virtual, and the object is complete
    return post;
}
```

During a base constructor the object's dynamic type is still the base, so a
virtual call there runs the base override rather than the derived one — quietly,
with no diagnostic. The factory moves the call to the first point where the
object is what it will be.
