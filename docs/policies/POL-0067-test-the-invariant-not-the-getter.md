---
id: POL-0067
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing: test the invariant, not the getter"
---

# Test the invariant, not the accessor

A validating constructor gets a test for each way its invariant can be violated
(POL-0022). An accessor that returns a member gets none.

```cpp
// Yes: the constructor decided something, and this is what it decided
TEST_CASE("RetryPolicy rejects a non-positive attempt count") {
    CHECK_THROWS_AS(RetryPolicy(0, 100.0, 0.1), std::invalid_argument);
}

// No: this asserts that a member initializer ran
TEST_CASE("max_attempts returns max_attempts") {
    CHECK(RetryPolicy(3, 100.0, 0.1).max_attempts() == 3);
}
```

The rule follows from where the decisions are. A constructor that rejects input
made a choice about what is valid, and that choice is what a later edit can
change without noticing. An accessor made no choice, so a test of it asserts
that the compiler assigned a member.

Accessor tests are cheap to write in bulk, which is why they accumulate, and
every one of them has to be maintained through a rename that a compiler would
have caught anyway. Their real cost is the reading: a suite where most tests
assert nothing trains whoever reads it to skim, and the invariant test that
matters is in the same file.
