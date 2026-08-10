---
id: POL-0081
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines: lambda captures"
---

# A lambda used as a coroutine captures by value

Captures into a coroutine lambda are by value. Capture by reference only where
the lambda's lifetime is provably bounded by the lifetime of what it captured,
and `[&]` is never that proof.

```cpp
// Never
auto task = [&]() -> Task<void> { co_await send(endpoint); }();

// Instead
auto task = [endpoint]() -> Task<void> { co_await send(endpoint); }();
```

The lambda's closure object is a second lifetime alongside the coroutine frame,
and both outlive the statement that created them. `this` capture is the case
most often missed: it is a reference capture, and a coroutine that captures
`this` outlives the object exactly as easily as one that captures a local.

This is POL-0080 one level out, and it is harder to see because the capture list
is not a parameter list. A reference capture in an ordinary lambda is bounded by
the call that invokes it, which is what makes `[&]` a reasonable habit
everywhere else. Suspension removes that bound without changing the syntax, so
the same three characters that were safe in the function above are a dangle
here, and nothing in the declaration marks the difference.
