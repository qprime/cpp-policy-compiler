---
id: POL-0170
kind: standard
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.21"]
---

# Several mutexes are acquired in one `std::scoped_lock`

```cpp
const std::scoped_lock lock(left.mutex_, right.mutex_);

const std::scoped_lock first(left.mutex_);      // no
const std::scoped_lock second(right.mutex_);
```

Two separate acquisitions can be interleaved by a thread taking them in the other
order, which deadlocks both. `std::scoped_lock` over several mutexes uses a
deadlock-avoiding algorithm, so the order the arguments appear in stops mattering.
