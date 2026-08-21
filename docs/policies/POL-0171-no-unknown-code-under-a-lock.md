---
id: POL-0171
kind: standard
trigger: "call code you do not control while holding a lock"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.22"]
---

# Never call a callback, a virtual function, or any code you do not control while holding a lock

Copy what you need, release the lock, then call out.

```cpp
std::vector<Warning> pending;
{
    const std::scoped_lock lock(mutex_);
    pending.swap(pending_);
}
for (const Warning& warning : pending) { observer_(warning); }   // lock released
```

Code you do not control may block, may take another lock, or may call back into
this object and try to take the same one. Any of the three deadlocks, and which one
happens depends on a callback that was registered somewhere else entirely.
