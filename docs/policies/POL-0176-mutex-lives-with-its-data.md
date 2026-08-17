---
id: POL-0176
kind: pattern
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.50"]
---

# A mutex is declared with the data it guards, and nothing else reaches that data

Put the mutex and the guarded members in one small type, private, and expose only
operations that take the lock. The type's name says what is guarded.

```cpp
class WarningLog {
 public:
    void add(Warning warning) {
        const std::scoped_lock lock(mutex_);
        warnings_.push_back(std::move(warning));
    }

    std::vector<Warning> drain() {
        const std::scoped_lock lock(mutex_);
        return std::exchange(warnings_, {});
    }

 private:
    std::mutex mutex_;
    std::vector<Warning> warnings_;
};
```

A mutex declared next to unrelated members leaves *what does this guard* to
convention, so the next author adds a member and does not know whether to lock. One
type per guarded group makes the answer structural, and makes an unguarded access
impossible to write from outside.
