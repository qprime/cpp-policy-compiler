---
id: POL-0172
kind: standard
trigger: "start a thread"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.23", "CG CP.24", "CG CP.25", "CG CP.26"]
---

# A thread is owned by an object that joins it in its destructor; nothing is detached

Use `std::jthread`, or a class holding a `std::thread` that joins in its
destructor. Treat a joining thread as scoped: everything it captures must outlive
the scope.

```cpp
class ScanThread {
 public:
    explicit ScanThread(Machine& machine) : worker_(&run_scan, std::ref(machine)) {}
    ~ScanThread() { if (worker_.joinable()) { worker_.join(); } }

 private:
    std::thread worker_;
};
```

A `std::thread` destroyed while joinable calls `std::terminate`. A detached thread
outlives every scope, so it becomes a global container: it may still be running
during static destruction, referring to objects that no longer exist, and nothing
can wait for it or report its failure.
