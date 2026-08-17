---
id: POL-0240
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# A test targets the function or class that holds the logic

Unit tests address the smallest thing that owns the behaviour. Pipeline tests are
integration tests: keep a few, covering that the pieces connect, not what each piece
computes.

```cpp
TEST_CASE("inset shrinks a convex ring by the offset") {
    const auto poly = ConvexPolygon::try_from(square_mm(100.0));
    REQUIRE(area_mm2(inset(*poly, 10.0)) == Approx(6400.0));
}

TEST_CASE("planning a job produces the expected paths") {   // integration: few of these
    REQUIRE(plan(load_job("fixtures/pocket.json")).size() == 42);
}
```

A failure in a unit test names the function that broke. The same defect reached
through the pipeline names the pipeline, and the author bisects to find what the
unit test would have said outright.
