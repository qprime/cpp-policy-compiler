---
id: POL-0140
kind: standard
attribution:
  - source: standard-practice
    locator: "concurrency, critical sections"
    upstream: ["CG CP.22", "CG CP.43", "CG CP.44"]
---

# A lock is named, held briefly, and never held across a call you do not control

```cpp
// Never. The callback may lock something else, re-enter, or block indefinitely.
{
    const std::lock_guard lock(m_);
    for (const auto& observer : observers_) { observer.on_change(state_); }
}

// Right. Copy what is needed, release, then call out.
std::vector<Observer> targets;
{
    const std::lock_guard lock(m_);
    targets = observers_;
}
for (const auto& observer : targets) { observer.on_change(state_); }
```

Every lock object has a name. `std::lock_guard(m_)` without one is a temporary
that is destroyed at the end of the full expression, so it locks and immediately
unlocks and the section that follows is unprotected. Nothing warns.

Do only what the shared state requires while holding the lock. Formatting,
allocation, and input or output belong outside it.

An unknown callee under a lock is the general case of deadlock: it may acquire a
second mutex in the opposite order to some other path (POL-0106), it may block
on input, or it may re-enter this object and try to take the same lock. None of
that is visible from the call, because the callee is chosen by whoever
registered it.

A long critical section serializes every other thread onto this one, which
converts a concurrency design into a sequential one that also pays for locking.
