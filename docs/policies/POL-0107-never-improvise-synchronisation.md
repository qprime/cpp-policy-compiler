---
id: POL-0107
kind: anti-pattern
replacement: [POL-0105]
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "§10 Concurrency, forbidden in every standard"
  - source: standard-practice
    locator: "concurrency, improvised synchronisation"
    upstream: ["CG CP.8"]
---

# Never improvise synchronisation out of `volatile`, a flag, or a sleep

```cpp
// Never. volatile orders nothing between threads.
volatile bool ready_ = false;

// Never. Double-checked locking without atomics is a data race.
if (!initialised_) {
    const std::lock_guard<std::mutex> lock(m_);
    if (!initialised_) { init(); initialised_ = true; }
}

// Never. Waiting by guessing.
while (!ready_) { std::this_thread::sleep_for(std::chrono::milliseconds(10)); }
```

Take the mechanism the need selects (POL-0105): `std::atomic` for the flag,
`std::call_once` or a function-local `static` for the one-time init,
`std::latch` or `atomic::wait` for the wait.

`volatile` addresses memory that changes outside the program — a
memory-mapped device register. It orders nothing and prevents no reordering
between threads, so it looks like synchronisation and provides none.

All three test as working. A data race is undefined behaviour whose observable
result depends on the optimizer, the core count, and the load, so the version
that passed on a developer machine is not evidence about the deployment host.
The sleep is the same defect with a tunable failure rate, which invites raising
the number rather than fixing the wait.
