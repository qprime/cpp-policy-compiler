cpp20-gcc-application › Logging

Read when: emitting diagnostics from library or application code.

## MUST — No `std::cout` or `printf` in library code

POL-0073

Console output belongs in a CLI entry point. A library reports through its
return values, its errors, and its logger, and writes to a stream nobody
configured.

```cpp
// Never, in a library
std::cout << "compacting " << segments.size() << " segments\n";

// Instead
logger.info("compacting {} segments", segments.size());
```

`printf`-family calls are additionally not type-safe and are permitted only
where the project has no `std::format` and a measured reason to avoid streams.

A library does not know what its output stream is for. The caller may be
producing machine-readable output on it, may have redirected it, or may be one
of a thousand invocations in a loop, and none of that is visible from inside the
library. One line left in a deep helper prints on every call thereafter, cannot
be turned off without an edit, and corrupts any consumer parsing that stream.
The logger exists so the decision about where output goes stays with the
application that knows.

## MUST — Use a structured logger

POL-0074

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

## SHOULD — Log levels have fixed meanings

POL-0075

| Level | Use when |
|-------|----------|
| `TRACE` / `DEBUG` | Internal state during development: values, branch taken |
| `INFO` | High-level progress. Operators read this; do not flood it with per-item detail |
| `WARN` | Unexpected but recoverable. Never for an expected situation |
| `ERROR` | Something failed and the program continues |
| `FATAL` | The program cannot continue |

Two lines separate the levels that get confused. Between `INFO` and `DEBUG`:
whether a person supervising the run needs it, not whether it was interesting to
whoever wrote it. Between `WARN` and `INFO`: whether it was expected. A retry
that the policy provides for is expected.

Every message carries the four parts where it reports a failure (POL-0011).

The level is the only filter anyone has, so it is what decides whether a message
is seen at all. Per-item detail logged at `INFO` does not add information, it
removes it, by pushing the lines an operator was watching for off the top of a
scroll. A `WARN` on an expected condition costs more: it fires on every normal
run, is learned to be ignorable within a week, and takes the rest of the level
with it, so the one genuine warning arrives in a channel nobody reads.
