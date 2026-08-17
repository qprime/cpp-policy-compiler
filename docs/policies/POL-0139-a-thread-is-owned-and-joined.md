---
id: POL-0139
kind: standard
attribution:
  - source: standard-practice
    locator: "concurrency, thread ownership"
    upstream: ["CG CP.23", "CG CP.24", "CG CP.26"]
---

# Every thread is owned by a scope that joins it

```cpp
// Never. Nothing waits for it, and nothing knows what it still refers to.
std::thread(scan_loop, std::ref(context)).detach();

// Right, on C++20. Joins in its destructor, on every path out.
std::jthread worker(scan_loop, std::ref(context));
```

Below C++20 the equivalent is a type holding a `std::thread` that joins in its
destructor, which is POL-0003 applied to a thread.

Never `detach()`. A detached thread outlives every scope, so it is a global with
an execution context attached, and it may still be running while the objects it
captured are destroyed during shutdown.

A joining thread is a scoped container: what it borrows must outlive the join,
and the join is what proves it. A detached one is unbounded, and no reader can
say what is still alive when the process exits.

A `std::thread` destroyed while still joinable calls `std::terminate`. That
turns any exception on the path between construction and `join()` into a process
abort, so the failure mode of forgetting the join is not a leak but a crash with
no unwinding and no diagnostic pointing at the thread.
