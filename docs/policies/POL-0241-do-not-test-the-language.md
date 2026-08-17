---
id: POL-0241
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# Do not test the language or the standard library

Test what your code adds. No test asserting that a `const` member cannot be
assigned, that an optional is empty by default, or that `std::vector` grows.

```cpp
TEST_CASE("a zero-diameter tool is rejected") {          // our invariant
    REQUIRE_THROWS_AS(Tool(0.0, 1200.0), std::invalid_argument);
}

TEST_CASE("a default optional is empty") {               // the language's guarantee
    REQUIRE(!std::optional<Tool>{}.has_value());
}
```

The second test cannot fail for any reason within your control, so it consumes
review attention and CI time and reports nothing. It also implies to the next reader
that the guarantee is in doubt, which invites more of the same.
