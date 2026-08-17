---
id: STD-0029
group: toolchain
enforced_by: build
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# One test framework per project, declared in the build

Catch2, GoogleTest, or doctest. Pick one at project start and use it everywhere. No
hand-rolled `int main()` runner, no `PASS`/`FAIL` prints, no second framework added
for one convenient macro.

```cmake
find_package(Catch2 3 REQUIRED)
target_link_libraries(proj_tests PRIVATE Catch2::Catch2WithMain)
```

Two frameworks in one repository means two ways to write a test, two runners for CI
to invoke, and two sets of output for a reader to learn.
