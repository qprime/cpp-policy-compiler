---
id: POL-0081
kind: standard
attribution:
  - source: standard-practice
    locator: "polymorphic copying"
    upstream: ["CG C.67", "CG C.130"]
---

# A polymorphic class suppresses public copy and move, and clones instead

Delete public copy and move on any class with virtual functions. Where callers
need a duplicate, give them a virtual `clone`.

```cpp
class PostProcessor {
 public:
    virtual ~PostProcessor() = default;
    virtual std::unique_ptr<PostProcessor> clone() const = 0;

    PostProcessor(const PostProcessor&) = delete;
    PostProcessor& operator=(const PostProcessor&) = delete;

 protected:
    PostProcessor() = default;
};
```

Copying through a base reference copies only the base part and leaves the derived
state behind, producing an object whose dynamic type disagrees with its contents.
`clone` returns the whole object because the override knows what the whole object
is.
