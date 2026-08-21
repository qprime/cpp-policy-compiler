---
id: POL-0191
kind: standard
trigger: "report failure through a global or a thread-local"
attribution:
  - source: standard-practice
    locator: "error reporting"
    upstream: ["CG E.28"]
---

# Failure is reported in the return value, never in global or thread-local state

No `errno`-style flag, no `last_error()`, no `get_error()` to call afterwards. Where
a C API uses one, read it immediately and convert.

```cpp
Result<Job, ParseError> parse_job(std::string_view text);

bool parse_job(std::string_view text, Job* out);   // and set g_last_error: no
```

Global error state is a return value with no connection to the call, so nothing
forces a caller to read it and nothing stops an intervening call from overwriting
it. It is also unusable from two threads without more machinery than returning the
error would have cost.
