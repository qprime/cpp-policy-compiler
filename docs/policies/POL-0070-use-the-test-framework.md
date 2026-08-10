---
id: POL-0070
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing: use the framework"
---

# Use the project's test framework

Tests use the framework the project declared — Catch2, GoogleTest, or doctest.
No hand-rolled `int main()` runner, no `PASS` and `FAIL` prints, no manual
counting of results.

```cpp
// Never
int main() {
    if (checksum(bytes) != expected) { std::cout << "FAIL\n"; return 1; }
    std::cout << "PASS\n";
}

// Instead
TEST_CASE("checksum matches the known vector") {
    CHECK(checksum(bytes) == expected);
}
```

Which framework is a per-project choice. That there is one is not.

A hand-rolled runner has no discovery, no filtering, no per-case isolation, and
no machine-readable output, so it cannot be run selectively while debugging and
cannot be aggregated with the rest of the suite. It also fails open: a case that
throws takes the process down before the later cases run, and the report says
nothing about the cases that never executed. The framework is where all of that
is already solved, which is why writing around it produces a suite that costs
more and reports less.
