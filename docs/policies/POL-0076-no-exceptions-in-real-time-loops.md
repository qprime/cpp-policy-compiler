---
id: POL-0076
kind: standard
applicability:
  domain: [realtime]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Real-Time Loops, Exceptions"
    upstream: ["CG E.25", "CG E.26", "CG E.27"]
---

# No exceptions in a real-time loop

Nothing inside a scan loop, an audio callback, or an interrupt handler throws,
and nothing it calls throws. Failures are recorded and surfaced at the boundary
instead (POL-0077).

The loop follows the exception-free discipline: RAII simulated by hand where the
compilation mode removes it, error codes used systematically under one
convention per module, and failing fast where that is the right answer. The
convention is stated in the module's top-level header (POL-0039).

Where the loop calls into code that may throw, the call is wrapped at the
boundary of the loop, not inside it. A `catch` inside the loop is the same
defect as the `throw`.

Throwing has no bound on how long it takes. Unwinding walks frames, consults
tables, and runs destructors, and how much of that happens depends on where the
handler is, which is a property of the call stack rather than of the loop. That
makes the cost unbounded in exactly the place where a bound is the requirement.
The failure is not a wrong answer; it is a deadline missed under load, arriving
late in a run and not in the test.
