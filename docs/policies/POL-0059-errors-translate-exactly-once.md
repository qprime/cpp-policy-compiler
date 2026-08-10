---
id: POL-0059
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions: errors translate exactly once"
---

# Errors translate exactly once, at the binding layer

A C++ exception becomes a host-language error at the binding layer, and nowhere
else. No exception crosses the seam unhandled, and no layer below the binding
catches in order to re-throw a different type (POL-0053).

The host side does not re-wrap what it receives. Type and message are preserved
across the translation, so the four-part message (POL-0011) that was constructed
in C++ is the one the user reads.

```
C++            throw std::invalid_argument("RetryPolicy: max_attempts must be > 0, got 0")
binding layer  translate to the host language's exception, message intact
host           the same four parts, in the host language's error type
```

One translation point is what keeps the failure attributable. Each additional
wrap replaces a matchable type with a string and prepends a layer name, so the
top of the stack receives a message assembled from prefixes and no way to
identify where the failure came from. An unhandled exception crossing the seam is
worse than either: the behaviour is undefined, so a diagnosable failure becomes a
crash with no message at all.
