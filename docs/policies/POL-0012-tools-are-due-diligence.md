---
id: POL-0012
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG P.12"]
---

# Tools run in the build and their findings block merge

Warnings, sanitizers, and static analysis run as part of the build, not on
request. A finding is a defect until someone explains otherwise, and every
per-site suppression carries a comment saying why.

```cpp
// NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
// extern "C" callback hands us the context as void*; the cast is the ABI.
auto* machine = reinterpret_cast<Machine*>(context);
```

A finding that does not block is a finding nobody reads. The suppression comment
is the part that matters: it converts a silent exemption into a reviewable
claim.

Tools are due diligence, not how quality is produced. A codebase that needs its
linter to be well-designed is not well-designed.
