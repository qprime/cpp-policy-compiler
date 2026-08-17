---
id: POL-0168
kind: pattern
attribution:
  - source: standard-practice
    locator: "shared ownership cycles"
    upstream: ["CG R.24"]
---

# Weak back-reference

```cpp
class Node {
 public:
    void attach(const std::shared_ptr<Node>& child) {
        child->parent_ = shared_from_this();
        children_.push_back(child);
    }
 private:
    std::vector<std::shared_ptr<Node>> children_;
    std::weak_ptr<Node> parent_;
};
```

Where shared ownership forms a cycle, exactly one direction is `std::weak_ptr`.
The owning direction is the one the structure is named for — a parent owns
children, a registry owns entries — and the back-reference is weak.

A `std::weak_ptr` is used by `lock()`, which returns a `std::shared_ptr` that is
empty if the object is gone. That check is the point: the back-reference states
in the type that the referent may already have been destroyed.

Two `std::shared_ptr`s pointing at each other never reach a reference count of
zero, so neither destructor runs. The leak is silent and total — the objects and
everything they own stay alive for the life of the process, and no sanitizer
reports it, because from the allocator's view the memory is still reachable.

Reaching this at all is a signal. POL-0048 makes `std::shared_ptr` the exception,
and a cycle usually means the ownership question has not been answered — one side
is an observer, and a raw reference or a `std::weak_ptr` says so.
