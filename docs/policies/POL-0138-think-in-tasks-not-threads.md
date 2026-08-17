---
id: POL-0138
kind: guideline
attribution:
  - source: standard-practice
    locator: "concurrency, tasks rather than threads"
    upstream: ["CG CP.4", "CG CP.41", "CG CP.60", "CG CP.61"]
---

# Concurrency is expressed as tasks with results, not as threads with side effects

```cpp
// Avoid. A thread, a shared buffer, and a lock to protect what is really a return value.
std::vector<Plan> results;
std::mutex m;
std::thread t([&] { auto p = plan(pocket); std::lock_guard lk(m); results.push_back(p); });

// Prefer. The result comes back through the type system.
auto future = std::async(std::launch::async, plan, pocket);
const auto p = future.get();
```

Prefer a pool or `std::async` to creating and destroying threads per unit of
work. Thread creation is expensive relative to most tasks, and a thread per item
turns a bounded workload into unbounded contention.

A task returns its result through a `std::future`, which means the answer
crosses the thread boundary as a value rather than as shared mutable state
someone has to lock, publish, and remember to read.

Thinking in threads makes every result a side effect on state two threads can
see, which is the sharing POL-0105 then has to protect. Thinking in tasks
removes most of that state: what would have been a guarded buffer becomes a
return type, and the concurrency question shrinks to what genuinely must be
shared (POL-0124).
