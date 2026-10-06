---
id: POL-0043
kind: guideline
trigger: "take or store a C-style string"
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions"
    upstream: ["CG F.25", "CG SL.str.3"]
---

# A C-style string is converted at the boundary and never carried inward

Where a foreign signature hands over `const char*`, wrap it once on entry —
`std::string_view` in C++17 and later when every use stays within the buffer's lifetime,
`std::string` when it does — and let the interior see only that.

```cpp
extern "C" int load_job_c(const char* path) noexcept {
    if (path == nullptr) { return kErrInvalidArgument; }
    try {
        return load_job(std::string(path)) ? kOk : kErrLoadFailed;
    } catch (...) {
        return kErrLoadFailed;
    }
}
```

A `const char*` travelling inward carries an unstated length, an unstated
encoding, and an unstated lifetime. `gsl::zstring` would name the convention and
is not worth a third-party dependency; conversion at the seam removes the
question instead of labelling it. In C++14, use an owning string or the project's
explicitly bounded view. The API must still require an accessible null-terminated
buffer, or accept a length and validate that contract; a null check cannot prove
that an arbitrary foreign pointer is readable. Translate exceptions from string
construction and the operation into the C API's error contract before returning.
