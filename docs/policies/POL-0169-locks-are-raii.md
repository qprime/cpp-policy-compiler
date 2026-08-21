---
id: POL-0169
kind: standard
trigger: "lock a mutex"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.20"]
---

# A lock is a named RAII object; never a bare `lock()`/`unlock()` pair

`std::scoped_lock` for one or more mutexes, `std::unique_lock` when the lock must be
released early or handed to a condition variable. Give it a name.

```cpp
{
    const std::scoped_lock lock(mutex_);
    tools_.push_back(tool);
}

mutex_.lock();
tools_.push_back(tool);        // a throw here never unlocks
mutex_.unlock();
```

The manual pair has to be matched on every exit, including the ones that throw, and
a missed `unlock` deadlocks the whole program rather than failing locally.
