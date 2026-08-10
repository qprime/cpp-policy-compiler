---
id: POL-0074
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Logging: use a structured logger"
---

# Use a structured logger

Logging goes through the project's chosen logging library, with the message and
its values passed as separate arguments rather than concatenated into a string
before the call.

```cpp
// Never: one opaque string, and the formatting cost is paid even when filtered out
logger.info("compacted " + std::to_string(n) + " segments in " +
            std::to_string(elapsed_ms) + "ms");

// Instead: the values stay values
logger.info("compacted {} segments in {}ms", n, elapsed_ms);
```

Which library is a per-project choice. That there is one, configured once, is
not.

Log lines built by concatenation are strings by the time anything sees them, so
a consumer that wants the count has to parse it back out of prose that was never
specified. Any change to the wording then breaks the consumer silently. Passing
the values separately also defers the formatting until the level is known to be
enabled, which is what keeps a disabled debug line from costing an allocation on
every iteration.

A log line failing is not a reason for an operation to fail. A logger that
throws or blocks has made the diagnostic more dangerous than the thing it was
diagnosing.
