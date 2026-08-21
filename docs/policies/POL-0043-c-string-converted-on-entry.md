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
`std::string_view` when the call does not outlive the caller's buffer,
`std::string` when it does — and let the interior see only that.

```cpp
extern "C" int load_job_c(const char* path) {
    if (path == nullptr) { return kErrInvalidArgument; }
    return load_job(std::string(path)) ? kOk : kErrLoadFailed;
}
```

A `const char*` travelling inward carries an unstated length, an unstated
encoding, and an unstated lifetime. `gsl::zstring` would name the convention and
is not worth a third-party dependency; conversion at the seam removes the
question instead of labelling it.
