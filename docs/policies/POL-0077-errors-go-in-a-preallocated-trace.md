---
id: POL-0077
kind: standard
applicability:
  domain: [realtime]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Real-Time Loops, Errors"
  - source: cpp-convention/conventions.md
    locator: "Failure semantics by layer, real-time loop"
---

# Real-time errors are recorded in a pre-allocated trace and surfaced at the boundary

A failure inside the loop writes into a trace structure allocated before the
loop was entered (POL-0012), and the loop continues. Nothing throws, nothing
allocates, and nothing decides to stop.

The caller outside the loop inspects the accumulated trace and decides whether
to halt. That is where the decision belongs, because it is the only place with
somewhere to report to and something to do.

The trace has a fixed capacity, so it also has a defined behaviour when full:
either the oldest entries are overwritten or a saturating counter records the
overflow, chosen per project and stated where the trace is defined. A trace that
silently drops entries is a silent wrong answer about what happened
(POL-0002).

A failure inside a deadline-bounded loop has no way to be reported at the moment
it occurs. Reporting takes formatting, locking, or allocation, and each of those
is unbounded; stopping the loop to report it is usually worse than the failure.
Recording into memory that already exists costs a store and defers everything
expensive to the boundary, which is the only point in the design where time is
available.
