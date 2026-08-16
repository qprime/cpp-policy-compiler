---
id: POL-0108
kind: anti-pattern
replacement: [POL-0105]
attribution:
  - source: cpp-convention/mechanisms.md
    locator: "§10 Concurrency, forbidden in every standard"
---

# Never keep thread-local global state

```cpp
// Never. Nothing in any signature says the result depends on which thread ran it.
thread_local ScanContext g_context;

void record(const Move& m) { g_context.moves.push_back(m); }

// Right. The dependency is a parameter.
void record(ScanContext& context, const Move& m) { context.moves.push_back(m); }
```

Where per-thread state is genuinely required, it lives in an explicit context
object created at the thread's entry point and passed into the functions that
need it.

Thread-local state is invisible in every signature that depends on it, so the
same call with the same arguments produces different results per thread and
nothing in the code says so. That defeats the determinism POL-0007 asks for and
makes the functions untestable in the ordinary way, because the test has to
reproduce which thread ran.

It also fails silently under a thread pool, where work migrates between threads
between calls and the state a function expects to find is the state some
unrelated task left behind.
