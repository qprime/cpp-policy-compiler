---
id: POL-0105
kind: pattern
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "§10 Concurrency"
  - source: standard-practice
    locator: "concurrency mechanism selection"
    upstream: ["CG CP.110"]
---

# Concurrency mechanism

Reached only once a threading model exists. POL-0049 governs whether one should.

| Need | Mechanism |
|------|-----------|
| Shared primitive: counter, flag, single-pointer handoff | `std::atomic<T>` |
| Compound shared state | `std::mutex` under a scoped lock |
| Read-heavy access, measured rather than assumed | `std::shared_mutex` |
| Wait / notify | `std::latch`, `std::barrier`, `atomic::wait`; `std::condition_variable` below C++20 |
| One-time initialization | `std::call_once`, or a function-local `static` |
| An owned thread | `std::jthread`; below C++20, a type that joins in its destructor |
| Pure functions over immutable data | nothing |

```cpp
class ScanCounter {
 public:
    void record() { count_.fetch_add(1, std::memory_order_relaxed); }
    std::int64_t total() const { return count_.load(std::memory_order_relaxed); }
 private:
    std::atomic<std::int64_t> count_{0};
};
```

An atomic makes the single-value case correct without a critical section, and a
mutex is the only mechanism that makes several values change together. Choosing
between them is the whole decision, and reaching for the mutex by default costs
a lock the design did not need while reaching for the atomic by default leaves
compound state torn.

The wait and one-time-init rows exist because both have a hand-written form
that is a classic race: a predicate loop omitted against spurious wakeup, and
an initialized flag checked without synchronization. The language provides
both correctly, so neither is written by hand (POL-0008).
