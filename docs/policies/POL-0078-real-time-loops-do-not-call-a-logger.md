---
id: POL-0078
kind: standard
applicability:
  domain: [realtime]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Real-Time Loops, Logging"
  - source: cpp-convention/conventions.md
    locator: "Logging: real-time loops use trace structures"
---

# A real-time loop does not call a logger

Diagnostics from inside the loop go into the trace structure (POL-0077). The
logger is called at the scan boundary, by the code that reads the trace.

This holds for every level, including the ones normally considered free.
A disabled `DEBUG` call is not free if reaching that decision requires a lock,
and it is not free at all if the level is enabled by a configuration change
nobody associated with the loop.

Two costs make a logger unusable here and neither is visible at the call. The
formatting is unbounded — it allocates, it may take a lock, and it may block on
a sink whose latency belongs to a device or a filesystem. The contention is
worse: a logger shared with other threads makes the loop's timing depend on what
those threads are doing, which turns a bounded loop into one whose worst case is
determined elsewhere. Writing into the trace costs a store, and the formatting
happens where the deadline does not apply.
