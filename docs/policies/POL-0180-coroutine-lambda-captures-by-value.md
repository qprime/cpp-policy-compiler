---
id: POL-0180
kind: standard
applicability:
  language_version: ["20", "23"]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines"
    upstream: ["CG CP.51"]
---

# A lambda that is a coroutine captures by value, or is not a lambda

Prefer a named coroutine function taking parameters by value. Where a lambda must
be one, capture every variable explicitly and by value, and never capture `this`.

```cpp
Task<void> stream_job(Job job);                     // prefer this

auto task = [job]() -> Task<void> { co_await send(job); };     // by value
auto task = [&job]() -> Task<void> { co_await send(job); };    // dangles
```

The closure object is destroyed at the end of the full expression that created the
coroutine, while the coroutine frame lives until it completes. Every capture — by
reference or by value — lives in the closure, so the frame outlives the captures it
is still using.
