---
id: POL-0089
kind: guideline
trigger: "write a handle that stands in for one object"
attribution:
  - source: standard-practice
    locator: "smart pointer interface"
    upstream: ["CG C.109"]
---

# A handle that stands in for one object provides `*` and `->`

When a type's job is to own or refer to a single object, give it the pointer
operators so callers reach the object the way they reach it through every other
handle.

```cpp
class ClipperHandle {
 public:
    clipper_paths& operator*() const { return *handle_; }
    clipper_paths* operator->() const { return handle_; }

 private:
    clipper_paths* handle_;
};
```

Callers already know `*` and `->`. A `get_underlying()` accessor does the same job
in a spelling nobody can guess and does not work in generic code written against
pointer-like types.
