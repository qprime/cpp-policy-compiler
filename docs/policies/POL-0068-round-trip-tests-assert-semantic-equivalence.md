---
id: POL-0068
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing: round-trip tests assert semantic equivalence"
---

# Round-trip tests assert semantic equivalence

A round-trip test asserts `parse(format(model)) == model`. It does not assert
that the text produced matches the text consumed.

Whitespace, key order, quoting style, and equivalent numeric spellings may
legitimately differ, and a test that forbids them is testing the formatter's
current output rather than the pair's agreement.

Where the model has no equality operator, the comparison is against a normalized
form, defined once and used by every round-trip test rather than restated per
test.

Comparing text asserts a property neither function promised, so it fails on
changes that are correct and passes on changes that are not. A formatter that
starts emitting two spaces breaks it, which is a false alarm that trains whoever
sees it to regenerate the expectation rather than read it. Meanwhile a parser
that drops a field the formatter never emits leaves the text identical and the
model wrong, which is the defect the round trip existed to catch.
