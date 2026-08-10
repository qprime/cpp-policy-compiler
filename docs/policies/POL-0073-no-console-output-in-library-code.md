---
id: POL-0073
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Logging: no std::cout or printf in library code"
  - source: cpp-convention/mechanisms.md
    locator: "§11 Strings and formatting, never in library code"
---

# No `std::cout` or `printf` in library code

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
