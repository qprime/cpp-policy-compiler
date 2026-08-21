---
id: POL-0242
kind: standard
trigger: "test an accessor that returns a member"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# Test the invariant; an accessor that returns a member needs no test

A validating constructor deserves a test for every input it must reject. An accessor
that returns what was stored does not.

```cpp
TEST_CASE("Tool rejects a negative rpm") {
    REQUIRE_THROWS_AS(Tool(6.0, -1.0), std::invalid_argument);
}

TEST_CASE("diameter_mm returns the diameter") {          // tests the compiler
    REQUIRE(Tool(6.0, 1200.0).diameter_mm() == Approx(6.0));
}
```

The accessor test passes on every implementation that compiles, so it can only fail
if someone changes the accessor to do something — at which point the test tells you
it changed, not whether the change was wrong. The invariant test is the one that
holds the design in place.
