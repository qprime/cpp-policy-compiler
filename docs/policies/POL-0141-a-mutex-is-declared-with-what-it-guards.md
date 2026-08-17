---
id: POL-0141
kind: pattern
attribution:
  - source: standard-practice
    locator: "concurrency, mutex placement"
    upstream: ["CG CP.50"]
---

# Guarded state

```cpp
class ToolCache {
 public:
    std::optional<Tool> find(ToolId id) const {
        const std::lock_guard lock(guard_.m);
        const auto it = guard_.by_id.find(id);
        return it == guard_.by_id.end() ? std::nullopt : std::optional{it->second};
    }

 private:
    struct Guarded {
        mutable std::mutex m;
        std::unordered_map<ToolId, Tool> by_id;
    };
    Guarded guard_;
};
```

The mutex and everything it protects sit in one nested structure, declared
together. What the lock covers is then a fact about the declaration rather than
a convention a reader has to infer from which members happen to be touched under
it.

A mutex declared beside unrelated members says nothing about its scope. The
protected set lives in whoever wrote the locking, and it drifts the first time a
member is added — nobody can tell from the declaration whether the new one
belongs inside the lock, so half the accessors take it and half do not.

This applies only where POL-0049 has established that a threading model exists,
and it does not make the type thread-safe on its own: a caller that reads and
then writes still races unless the compound operation is itself a method
(POL-0105).
