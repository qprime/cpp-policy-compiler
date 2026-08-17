---
id: POL-0162
kind: standard
applicability:
  domain: ["realtime"]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Real-Time Loops"
    upstream: ["CG Per.30", "CG CP.40", "CG CP.41"]
---

# A deadline-bound path takes no lock of unbounded duration and does no I/O

No blocking calls, no logging through a runtime logger, no unbounded loops, no
waiting on another thread. Record into a pre-allocated trace and let the caller
inspect it at the scan boundary.

```cpp
void ScanLoop::step() {
    const Sample sample = read_encoders();
    if (sample.fault) { trace_.push_back(Event{EventKind::Fault, sample.axis}); }
    write_outputs(compute(sample));
}
```

A context switch costs microseconds at best and is unbounded when it depends on
another thread's progress. Formatting cost and lock contention in a logger are the
same problem wearing a friendlier name.
