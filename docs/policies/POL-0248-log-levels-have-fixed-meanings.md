---
id: POL-0248
kind: standard
trigger: "choose a log level"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Logging"
---

# Log levels have fixed meanings

| Level | Use when |
|-------|----------|
| `TRACE` / `DEBUG` | Internal state during development — values, branch taken |
| `INFO` | High-level progress. Operators read this; do not flood it with per-item detail |
| `WARN` | Unexpected but recoverable. Not for expected situations |
| `ERROR` | Something failed; the program continues |
| `FATAL` | The program cannot continue |

```cpp
log_info("plan: {} faces, {} tools", job.faces.size(), job.tools.size());
log_warn("plan_pocket: step_over_mm {} exceeds face width {}", step, width);
log_info("skipping empty face");        // per-item detail: belongs at DEBUG
```

Levels are the only filter an operator has, so a `WARN` used for an expected
situation trains them to ignore the level that was supposed to get their attention.
`INFO` carrying per-item detail does the same thing by volume.
