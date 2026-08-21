---
id: POL-0247
kind: standard
trigger: "finish a test suite for a behaviour"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# A suite that passes on a plausible wrong implementation is not testing

For each behaviour, ask what a plausible wrong implementation would look like and
check that some test rejects it. If none does, the behaviour is uncovered however
many tests mention it.

```cpp
TEST_CASE("inset shrinks a convex ring") {
    REQUIRE(inset(poly, 10.0).size() > 0);        // passes on a stub returning poly
    REQUIRE(area_mm2(inset(poly, 10.0)) == Approx(6400.0));   // rejects it
}
```

Assertions on shape rather than value — non-empty, right count, no throw — pass on an
implementation that returns its input unchanged. A suite made of them is green
against code that does nothing, which is the state it exists to detect.

Tests are due diligence, not a quality mechanism. A defect the type system can refuse
should never reach one.
