---
id: POL-0166
kind: standard
trigger: "start a thread to mutate state"
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "10. Concurrency"
    upstream: ["CG CP.4", "CG CP.60", "CG CP.61"]
---

# Express concurrent work as a task returning a value, not as a thread mutating state

Hand a unit of work to `std::async` or a task pool and take its result from the
returned `std::future`. Reach for a raw thread only when the work is a long-lived
loop rather than a computation.

```cpp
auto rough = std::async(std::launch::async, plan_rough, face, params);
auto finish = std::async(std::launch::async, plan_finish, face, params);
return combine(rough.get(), finish.get());
```

A task has one input and one output, so there is no shared state to guard and the
failure path is the future's exception. A thread writing into shared variables
turns the same work into a synchronization problem that has to be solved
separately.
