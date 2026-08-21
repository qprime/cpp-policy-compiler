---
id: POL-0050
kind: standard
trigger: "write main"
attribution:
  - source: standard-practice
    locator: "program entry point"
    upstream: ["CG F.46"]
---

# `main` returns `int`, and the value it returns means something

Write one of the two standard signatures and return a status the caller can
branch on. `EXIT_SUCCESS` and `EXIT_FAILURE`, or `0` and a small nonzero code
documented in the tool's help.

```cpp
int main(int argc, char** argv) {
    const Options options = parse_options(argc, argv);
    return run(options) ? EXIT_SUCCESS : EXIT_FAILURE;
}
```

Every shell, build system, and CI runner branches on that value. A `main`
returning success unconditionally makes a failed run indistinguishable from a
good one to everything outside the process.
