---
id: POL-0012
kind: standard
applicability:
  domain: [realtime]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Real-Time Loops, Allocation"
---

# Pre-allocate in real-time loops

Every buffer a real-time loop needs is allocated before the loop is entered.
Inside it, `push_back`, string operations that may reallocate, and anything
reaching `malloc` are defects unless proven otherwise.

"Proven otherwise" means an allocator with a documented worst-case bound, not an
observation that allocation has been fast so far. The burden sits on the
allocation.

Scan loops, audio callbacks, and interrupt handlers have a deadline, and
allocation has no bound on how long it takes. A heap that has never been slow
under test is a heap that has not yet fragmented. The failure this prevents is
not a wrong answer; it is a missed deadline, which arrives late in a run, under
load, and not in the test.
