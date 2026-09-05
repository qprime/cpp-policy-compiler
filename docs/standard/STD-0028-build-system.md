---
id: STD-0028
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
---

# CMake by default

```
CMakeLists.txt              # declares the standard, warnings, sanitizers
<layer>/CMakeLists.txt      # one target per layer
```

CMake is what the ecosystem's dependency tooling, IDE integrations, and CI actions
already assume, so departing from it costs integration work at every one of those
points.

A target project that replaces this canonical decision does so through a
project-owned standard overlay with its reason, rather than turning this entry
into a menu of build systems.
