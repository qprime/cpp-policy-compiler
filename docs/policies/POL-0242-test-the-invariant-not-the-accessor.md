---
id: POL-0242
kind: standard
trigger: "test an accessor that returns a member"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# Test the invariant; a trivial accessor usually needs no separate test

A validating constructor deserves a test for every input category it must reject.
An accessor already exercised while testing meaningful behavior usually does not
need its own test.

```cpp
TEST_CASE("Tool rejects a negative rpm") {
    REQUIRE_THROWS_AS(Tool(6.0, -1.0), std::invalid_argument);
}

TEST_CASE("diameter_mm returns the diameter") {          // tests the compiler
    REQUIRE(Tool(6.0, 1200.0).diameter_mm() == Approx(6.0));
}
```

A standalone accessor test can catch returning the wrong member, but often duplicates
the observation made by a behavior or invariant test. Add it when the mapping itself
is a public contract not otherwise exercised; do not test boilerplate merely to give
each method a test-shaped neighbor.
