---
id: POL-0075
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Logging: level table"
---

# Log levels have fixed meanings

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
