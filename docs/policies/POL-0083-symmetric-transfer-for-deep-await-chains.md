---
id: POL-0083
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines: co_await chains"
---

# Use symmetric transfer past two or three levels of `co_await`

Where coroutines await coroutines more than two or three levels deep,
`await_suspend` returns a `std::coroutine_handle<>` rather than resuming the
next coroutine itself.

```cpp
// Resumes inline: each resumption adds a frame to the stack
void await_suspend(std::coroutine_handle<> h) { continuation_.resume(); }

// Symmetric transfer: the caller resumes, and the current frame goes away first
std::coroutine_handle<> await_suspend(std::coroutine_handle<> h) { return continuation_; }
```

Two or three levels is where the shallow case ends, not a measured threshold.
The depth that matters is dynamic: a chain that is three levels in the source
and iterates is unbounded at runtime.

Resuming inline means each resumption is a call, so a chain of resumptions is a
chain of stack frames that only unwinds when the innermost completes. A loop
that awaits repeatedly then grows the stack in proportion to its iteration count,
which is a stack overflow whose cause is a `co_await` that looks like every
other one. Returning the handle lets the compiler tail-transfer, so the frame
being suspended is released before the next resumes and the depth stays flat
regardless of how long the chain runs.
