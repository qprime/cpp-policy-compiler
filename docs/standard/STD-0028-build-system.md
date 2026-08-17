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

An alternative is permitted and carries a stated reason in the repository's README.

CMake is what the ecosystem's dependency tooling, IDE integrations, and CI actions
already assume, so departing from it costs integration work at every one of those
points.
