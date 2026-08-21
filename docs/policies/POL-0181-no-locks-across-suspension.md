---
id: POL-0181
kind: standard
trigger: "hold a lock across a co_await"
applicability:
  language_version: ["20", "23"]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines"
    upstream: ["CG CP.52"]
---

# No lock or other synchronization primitive is held across a `co_await`

Take the lock, do the work, release it, then suspend.

```cpp
Task<void> record(Sample sample) {
    {
        const std::scoped_lock lock(mutex_);
        samples_.push_back(sample);
    }
    co_await flush();
}

Task<void> record(Sample sample) {
    const std::scoped_lock lock(mutex_);
    co_await flush();                      // resumes on another thread: UB
}
```

A coroutine may resume on a different thread from the one that suspended it, and a
`std::mutex` must be released by the thread that locked it. The lock is also held
for the whole suspension, which is unbounded — that is a deadlock with a timer on
it.
