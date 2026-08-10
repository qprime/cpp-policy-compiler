---
id: POL-0049
kind: anti-pattern
replacement: [POL-0028]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: cargo-culted mutex"
---

# Never add a mutex to a class with no threading model

A `std::mutex` member on a class nobody shares across threads protects nothing.
The default for every type is single-threaded by contract, and concurrent access
is the caller's problem until the type says otherwise.

```cpp
// Never: locks every accessor, documents nothing, and is not thread-safe anyway
class Registry {
 public:
    void add(Entry e) { std::lock_guard<std::mutex> lock(m_); entries_.push_back(std::move(e)); }
    std::vector<Entry> all() const { std::lock_guard<std::mutex> lock(m_); return entries_; }
 private:
    mutable std::mutex m_;
    std::vector<Entry> entries_;
};
```

Write nothing, and state the threading model at the module boundary when
concurrency is actually introduced (POL-0028).

A per-method lock makes each method atomic and makes nothing else atomic, so any
caller reading and then writing still races. The type is now advertised as
thread-safe, which is the claim that causes the race to be written. It costs a
lock on every access, it costs the reader an assumption about a model that was
never designed, and it removes the pressure to design one, because the mutex
looks like the design.
