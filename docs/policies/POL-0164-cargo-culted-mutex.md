---
id: POL-0164
kind: anti-pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: cargo-culted mutex"
replacement: ["POL-0163"]
---

# A `std::mutex` member added to make a class feel thread-safe

```cpp
class ToolTable {
 public:
    Tool at(int slot) const {
        std::scoped_lock lock(mutex_);
        return tools_.at(slot);            // safe per call, useless across calls
    }

 private:
    mutable std::mutex mutex_;
    std::vector<Tool> tools_;
};
```

Locking each accessor makes no sequence of accessors atomic, so a caller reading
two slots still sees a torn view. The class now pays for a lock on every call and
still cannot state what it guarantees.
