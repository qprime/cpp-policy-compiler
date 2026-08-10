---
id: POL-0079
kind: standard
applicability:
  domain: [realtime]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Real-Time Loops, Determinism"
---

# Every operation in a real-time loop has a bound

Three things are excluded outright:

- an unbounded loop, including one whose bound is a function of input the loop
  does not control
- acquiring a lock of unbounded duration, which is any lock a non-real-time
  thread can hold
- I/O of any kind

Each iteration's worst case has to be statable without running it. Where an
algorithm's cost depends on the data, the loop carries an explicit iteration cap
and records reaching it in the trace (POL-0077) rather than continuing.

"Measured and it was fast" is not a bound. A bound is an argument about the
worst case; a measurement is an observation about the cases that were run
(POL-0012).

A real-time loop's contract is the deadline, and a deadline is a claim about the
worst case rather than the usual one. An unbounded operation makes that claim
unprovable no matter how the loop behaves in testing, because the input that
exceeds it has not happened yet. Missing the deadline also fails differently
from producing a wrong answer: there is no incorrect output to catch downstream,
only a system that was late, which surfaces as behaviour nobody can attribute to
a line of code.
