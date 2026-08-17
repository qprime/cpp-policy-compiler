---
id: STD-0026
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments"
    upstream: ["CG P.12"]
---

# clang-tidy runs `bugprone-*`, `cert-*`, `cppcoreguidelines-*`, `performance-*`, `readability-*`

```yaml
# .clang-tidy
Checks: >
  bugprone-*,
  cert-*,
  cppcoreguidelines-*,
  performance-*,
  readability-*
WarningsAsErrors: '*'
```

A project-level disable lives in this file with one comment per disable. A per-site
`NOLINT` carries a comment on the same line or the line above.
