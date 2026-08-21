---
id: POL-0150
kind: standard
trigger: "write goto"
attribution:
  - source: standard-practice
    locator: "unstructured control flow"
    upstream: ["CG ES.76"]
---

# No `goto`

Use RAII for cleanup, early returns for guards, and a named function when the flow
is genuinely complicated.

```cpp
bool run(const Job& job) {
    SerialPort port(job.device);              // released on every exit
    if (!handshake(port)) { return false; }
    return stream_job(port, job);
}
```

`goto` exists in C to reach a cleanup label, and RAII removes that need entirely.
What remains is a jump that breaks the reader's ability to know how control got to
a line.
