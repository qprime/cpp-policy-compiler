---
id: POL-0022
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Divergences: [CG I.12], [CG F.23]"
    upstream: ["CG I.12", "CG F.23"]
---

# A pointer that must not be null is documented and asserted

Take a reference when the argument is mandatory. Where a pointer is forced —
optional-by-design, or a foreign signature — state the requirement and assert it
on entry.

```cpp
void configure(Machine& machine, const MachineConfig& config);   // both mandatory

// context is never null; the extern "C" signature forces the pointer.
extern "C" void on_tick(void* context) {
    assert(context != nullptr);
    ...
}
```

A reference is the type-level statement, so use it and the question disappears.
`gsl::not_null` would say it for the remaining cases and is not worth a
third-party dependency in an FFI kernel.
