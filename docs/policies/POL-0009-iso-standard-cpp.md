---
id: POL-0009
kind: standard
attribution:
  - source: standard-practice
    locator: "language extensions"
    upstream: ["CG P.2"]
---

# Write ISO standard C++; a compiler extension is a declared exception

Use only what the declared standard guarantees. Where a platform forces an
extension, isolate it behind an interface that names the platform and state the
dependency in that module's top-level header.

```cpp
#if defined(__GNUC__)
[[gnu::hot]] void scan_step(Machine& machine);   // extension, one site, declared
#else
void scan_step(Machine& machine);
#endif
```

An extension used inline spreads to every caller and is discovered on the day
the toolchain changes. Isolated, it is one file to port.
