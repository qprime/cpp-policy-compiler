---
id: POL-0245
kind: standard
trigger: "write a test"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# A test is written in the project's framework

Use whichever framework the project's build declares. No hand-rolled `int main()`
runner, no `PASS`/`FAIL` prints, no manual counting of results.

```cpp
TEST_CASE("inset shrinks a convex ring") {
    REQUIRE(area_mm2(inset(poly, 10.0)) == Approx(6400.0));
}

int main() {
    if (area_mm2(inset(poly, 10.0)) != 6400.0) { std::printf("FAIL\n"); return 1; }
    std::printf("PASS\n");
}
```

The hand-rolled runner stops at the first failure, reports no location, cannot be
filtered or listed, and returns nothing a CI system can summarize. Every framework
gives all of that for the same line count.
