---
id: POL-0167
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.8", "CG CP.200"]
---

# `volatile` is for memory outside the program; synchronization is `std::atomic`

Use `std::atomic<T>` between threads. Reserve `volatile` for a
memory-mapped device register or memory a signal handler or foreign process writes,
and do not use compound assignment on it.

```cpp
std::atomic<bool> stop_requested{false};              // between threads

volatile std::uint32_t* const status = device_status_register();   // hardware
```

`volatile` stops the compiler caching the value in a register and does nothing
else: it orders nothing, it is not atomic, and it emits no fences. Code using it
for synchronization is racy on every platform and happens to work on some.
