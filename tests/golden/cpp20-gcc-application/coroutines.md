cpp20-gcc-application › Coroutines

Read when: writing coroutines — lifetimes across suspension, captures, awaitables, deep chains. Vacuous below C++20.

## MUST — A coroutine that may suspend takes its parameters by value

POL-0080

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

## MUST — A lambda used as a coroutine captures by value

POL-0081

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

## SHOULD — Awaitables are non-owning by default

POL-0082

An awaitable refers to what it awaits and does not own it. The awaiting frame is
what keeps the operation alive for the duration of the suspension.

An awaitable that outlives the frame that awaited it is an ownership decision,
made explicitly and stated at the type. Detached work, a queued operation, or a
handle stored for later cancellation each need a named owner, chosen with
POL-0024 the same as any other resource.

The common failure is not writing the wrong owner. It is writing no owner: an
awaitable stored in a container so it can be cancelled later, with nothing
established about whether the frame it belongs to still exists.

The default is non-owning because that is what the ordinary case needs and it
costs nothing to express. Making the exception explicit is what keeps the two
cases distinguishable, since an awaitable that owns and one that does not are
identical at the await expression. Where the distinction is left implicit, the
lifetime question is answered by the scheduler, which answers it differently
under load.

## SHOULD — Use symmetric transfer past two or three levels of `co_await`

POL-0083

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
