---
id: POL-0074
kind: standard
attribution:
  - source: standard-practice
    locator: "destructor exception safety"
    upstream: ["CG C.36", "CG C.37", "CG E.16"]
---

# A destructor never throws, and neither does deallocation, `swap`, or an exception copy

Destructors are implicitly `noexcept`; leave it that way. Where cleanup can fail,
log or record the failure and continue releasing.

```cpp
SerialPort::~SerialPort() {
    if (::close(fd_) != 0) {
        record_close_failure(fd_, errno);   // never throw from here
    }
}
```

A destructor that throws during stack unwinding calls `std::terminate`, so the
original exception is never seen. The same reasoning covers deallocation, `swap`,
and copying an exception object: each runs at a point where the program has no
way left to report a second failure.
