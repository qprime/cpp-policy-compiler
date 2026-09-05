---
id: POL-0180
kind: standard
trigger: "write a lambda that is a coroutine"
applicability:
  language_version: ["20", "23"]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines"
    upstream: ["CG CP.51"]
---

# A coroutine lambda is captureless; state is passed as by-value parameters

Prefer a named coroutine function taking parameters by value. Where a lambda must
be a coroutine, make it captureless and pass each required value as a parameter so
the values are copied into the coroutine frame.

```cpp
Task<void> stream_job(Job job);                     // prefer this

auto stream = [](Job job) -> Task<void> { co_await send(job); };
auto task = stream(job);                              // parameter lives in frame

auto task = [job]() -> Task<void> { co_await send(job); }();  // capture dangles
```

The closure object can be destroyed after the call creates the coroutine, while the
coroutine frame lives until completion. Every capture — by reference or by value —
lives in that closure rather than becoming a parameter copy in the frame, so a
suspended coroutine can outlive what it still uses.
