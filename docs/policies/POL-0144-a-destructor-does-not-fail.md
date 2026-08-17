---
id: POL-0144
kind: standard
attribution:
  - source: standard-practice
    locator: "destructors"
    upstream: ["CG C.36", "CG C.37", "CG E.16"]
---

# A destructor cannot fail, and neither can `swap` or a deallocation

```cpp
// Never. If close() throws during unwinding, the program terminates.
~FileHandle() { close(fd_); }

// Right. Report at the point the caller can act; the destructor only releases.
~FileHandle() noexcept {
    if (fd_ >= 0) { ::close(fd_); }
}
void flush();  // the operation that can fail is a named operation the caller calls
```

A destructor is implicitly `noexcept`, and it is written to be true: everything
inside it either cannot throw or has its exception handled there.

The same holds for `swap`, for deallocation, and for the copy and move
constructors of an exception type — all four run on paths that have no way to
report a second failure.

A destructor that throws during stack unwinding calls `std::terminate`, so an
exception in flight plus a failing destructor is a process abort with no handler
and no unwinding. That means the failure mode of a throwing destructor is not a
propagated error but the loss of every error already being reported.

Where releasing a resource genuinely can fail in a way the caller must know
about, the fallible part is a named operation the caller invokes explicitly
(POL-0030). The destructor remains the last-resort release that always runs and
never reports.
