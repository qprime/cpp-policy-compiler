---
id: POL-0080
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines: reference parameters"
---

# A coroutine that may suspend takes its parameters by value

No reference or pointer parameter into a coroutine that can suspend. Parameters
are taken by value, so the coroutine frame owns what it reads after resumption.

```cpp
// Never: the caller's frame may be gone before the coroutine resumes
Task<Digest> checksum_async(const Buffer& buffer);

// Instead: the frame owns it
Task<Digest> checksum_async(Buffer buffer);
```

The rule is about suspension, not about coroutines in general. A coroutine that
provably completes before its caller's frame ends is not exempt in practice,
because the proof is a property of every caller and is lost the first time one is
added.

Coroutines are C++20. A project on an earlier standard has nothing here to apply.

A coroutine's parameters live in the frame, but a reference parameter puts only
the reference there and leaves the referent in the caller. Suspension breaks the
connection between the two lifetimes: the caller's frame unwinds while the
coroutine is waiting, and resumption then reads storage that has been reused. The
call site looks correct, the dangle happens at a point determined by scheduling,
and the read succeeds and returns other data rather than faulting.
