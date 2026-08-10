---
id: POL-0066
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing: do not test the language"
---

# Do not test the language or the standard library

No test asserting that a `const` member cannot be assigned, that a default-
constructed optional is empty, that a `unique_ptr` releases on destruction, or
that a `vector` grows when pushed to. Test what this code adds.

```cpp
// Never: this asserts a language guarantee
TEST_CASE("optional is empty by default") { CHECK(!std::optional<int>{}.has_value()); }

// Instead: this asserts something this code decided
TEST_CASE("load_entries returns nullopt for a missing path") {
    CHECK(!load_entries(Path{"does-not-exist"}).has_value());
}
```

The line is whether the assertion could fail without a change to this codebase.
If not, the test is asserting the compiler.

A test of a language guarantee cannot fail, so it contributes no information and
consumes the attention a real test would have received. It also misrepresents
coverage: a suite reporting a hundred passing tests where thirty assert the
standard library looks like a suite that checked thirty things it did not. The
form is worth naming because it is what gets written when the goal is a test
rather than a question about the code.
