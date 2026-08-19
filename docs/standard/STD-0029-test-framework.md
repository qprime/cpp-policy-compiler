---
id: STD-0029
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# The test framework is Catch2, declared in the build

```cmake
find_package(Catch2 3 REQUIRED)
target_link_libraries(proj_tests PRIVATE Catch2::Catch2WithMain)
```

No second framework beside it for one convenient macro. Two frameworks in one
repository means two ways to write a test, two runners for CI to invoke, and two sets
of output for a reader to learn.
