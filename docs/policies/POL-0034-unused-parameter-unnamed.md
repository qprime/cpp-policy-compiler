---
id: POL-0034
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: void-cast unused param"
    upstream: ["CG F.9"]
---

# An unused parameter is unnamed, or it should not exist

On a leaf function, delete the parameter. Where the signature is mandated — a
virtual override, a callback shape, an interface implementation — leave the type
and drop the name.

```cpp
std::string emit(const Move& move, const PostContext&) const override;

std::string emit(const Move& move, const PostContext& context) const override {
    (void)context;   // no
    ...
}
```

`(void)param;` silences the warning and preserves the lie that the parameter
matters. An unnamed parameter says the same thing to the compiler and tells the
reader the truth.
