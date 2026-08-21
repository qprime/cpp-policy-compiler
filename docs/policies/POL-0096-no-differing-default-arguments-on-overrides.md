---
id: POL-0096
kind: standard
trigger: "give a virtual function a default argument"
attribution:
  - source: standard-practice
    locator: "virtual default arguments"
    upstream: ["CG C.140"]
---

# A virtual function and its overriders declare the same default arguments, or none

Prefer none: give the base an overload that supplies the value and keep the
virtual function's parameter list complete.

```cpp
class PostProcessor {
 public:
    virtual std::string emit(const Move& move, bool verbose) const = 0;
    std::string emit(const Move& move) const { return emit(move, false); }
};
```

Default arguments are resolved from the static type, so calling through a base
reference uses the base's default while dispatching to the derived body. The same
call then means two different things depending on the declared type of the
handle.
