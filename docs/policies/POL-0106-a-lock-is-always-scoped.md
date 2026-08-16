---
id: POL-0106
kind: standard
attribution:
  - source: standard-practice
    locator: "concurrency, lock ownership"
    upstream: ["CG CP.20", "CG CP.21"]
---

# A mutex is locked by a scoped lock, never by hand

```cpp
// Never. Every early return and every throw leaks the lock.
m_.lock();
if (entries_.empty()) { return {}; }
auto result = entries_.front();
m_.unlock();

// Right.
const std::lock_guard<std::mutex> lock(m_);
if (entries_.empty()) { return {}; }
return entries_.front();
```

Locking more than one mutex at once takes `std::scoped_lock` over all of them
in one statement.

A hand-managed lock is a resource released on one path and leaked on every
other, which is exactly the case POL-0003 answers with RAII. The failure is
worse than a leak: the mutex stays held, so the next thread to want it blocks
forever, and the deadlock surfaces far from the return that caused it.

Two sequential `lock_guard`s in different orders in two functions deadlock
whenever both run at once. `std::scoped_lock` orders the acquisition
internally, so the ordering cannot be got wrong at the call site and does not
have to be documented and remembered.
