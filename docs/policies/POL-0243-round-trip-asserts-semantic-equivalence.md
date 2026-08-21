---
id: POL-0243
kind: standard
trigger: "write a round-trip test"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing"
---

# A round-trip test asserts semantic equivalence, not textual identity

Compare the parsed models, not the two strings. Whitespace, key order, and
equivalent representations of the same value may legitimately differ.

```cpp
TEST_CASE("a job survives format and parse") {
    const Job original = load_job("fixtures/pocket.json");
    REQUIRE(parse_job(format_job(original)) == original);

    REQUIRE(format_job(parse_job(text)) == text);        // brittle: asserts the spelling
}
```

The textual form pins decisions the format never promised — how many spaces, which
order, whether `1.0` prints as `1` — so a harmless change to the writer breaks a test
that was meant to cover the reader. Comparing models tests the property you actually
depend on.
