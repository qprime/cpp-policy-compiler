---
id: POL-0179
kind: standard
trigger: "declare a coroutine parameter"
applicability:
  language_version: ["20", "23"]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Coroutines"
    upstream: ["CG CP.53"]
---

# A coroutine takes its parameters by value

Copy or move everything the coroutine body needs. No reference parameters, no
pointers into the caller's frame.

```cpp
Task<Paths> plan_async(PlanarFace face, PocketParams params);

Task<Paths> plan_async(const PlanarFace& face, const PocketParams& params);   // no
```

A coroutine's parameters are copied into the coroutine frame, but a reference
parameter copies only the reference. The caller's frame is gone by the time the
coroutine resumes, so every use after the first suspension reads freed storage —
and it typically works until the first suspension actually happens.
