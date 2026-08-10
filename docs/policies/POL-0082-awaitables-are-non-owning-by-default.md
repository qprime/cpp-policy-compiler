---
id: POL-0082
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines: awaitable lifetime"
---

# Awaitables are non-owning by default

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
