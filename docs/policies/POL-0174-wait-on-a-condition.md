---
id: POL-0174
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.42"]
---

# A wait always names the condition it is waiting for

Pass the predicate to `wait`. Never wait bare, and never poll with `sleep_for`.

```cpp
std::unique_lock lock(mutex_);
queue_ready_.wait(lock, [this] { return !queue_.empty() || stopping_; });

queue_ready_.wait(lock);                    // wakes spuriously, proceeds anyway
while (queue_.empty()) { std::this_thread::sleep_for(1ms); }   // no
```

Condition variables wake spuriously, so a bare `wait` continues when nothing
happened and the code after it runs on a state that is not ready. The predicate form
re-checks and goes back to sleep. Polling with a sleep trades latency for CPU and
still races.
