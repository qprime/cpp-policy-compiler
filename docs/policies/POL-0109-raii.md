---
id: POL-0109
kind: pattern
trigger: "acquire a resource"
attribution:
  - source: standard-practice
    locator: "RAII"
    upstream: ["CG R.1", "CG E.6"]
---

# Every resource is held by an object whose destructor releases it

Acquire in a constructor, release in a destructor, and let scope do the rest. No
`open`/`close` pairs for a caller to match, no cleanup label, no release on the
error path.

```cpp
{
    SerialPort port("/dev/ttyUSB0");       // acquired
    port.write(preamble);
    if (!handshake(port)) { return false; }   // released here
    stream_job(port, job);
}                                             // released here
```

Every early return, every `break`, and every thrown exception releases the
resource, because the release is attached to the object rather than to a path
through the function. A hand-written cleanup path has to be correct once per exit,
and new exits get added by people who did not write the original.
