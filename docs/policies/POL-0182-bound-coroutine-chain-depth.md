---
id: POL-0182
kind: guideline
trigger: "chain more than two or three co_await hops"
applicability:
  language_version: ["20", "23"]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines"
---

# Beyond two or three `co_await` hops, use symmetric transfer

Return `std::coroutine_handle<>` from `await_suspend` rather than resuming the
continuation inside it.

```cpp
std::coroutine_handle<> await_suspend(std::coroutine_handle<> awaiting) noexcept {
    handle_.promise().continuation = awaiting;
    return handle_;                          // tail transfer, no stack growth
}
```

Resuming inside `await_suspend` calls the next coroutine on top of the current
frame, so a chain of awaits grows the stack in proportion to its depth. Returning
the handle lets the compiler tail-transfer instead, which keeps the stack flat
however deep the chain gets.

Awaitables are non-owning by default; one that outlives the awaiting frame is an
explicit ownership decision.
