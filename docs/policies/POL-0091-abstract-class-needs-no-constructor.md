---
id: POL-0091
kind: guideline
attribution:
  - source: standard-practice
    locator: "abstract class construction"
    upstream: ["CG C.126"]
---

# An abstract class usually needs no user-written constructor

With no data members there is nothing to initialize, so write none and let the
compiler's implicit one serve the derived classes.

```cpp
class PostProcessor {
 public:
    virtual ~PostProcessor() = default;
    virtual std::string emit(const Move& move) const = 0;
};
```

A hand-written constructor on a data-free abstract class is ceremony, and if it
takes arguments it is a sign the base is holding state — which makes it shared
implementation rather than an interface.
