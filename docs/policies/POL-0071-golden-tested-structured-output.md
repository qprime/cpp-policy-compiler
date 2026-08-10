---
id: POL-0071
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing: golden-tested IR"
---

# Structured output is golden-tested

Any computation producing structured output — a plan, a schedule, a trace, an
intermediate representation, generated code — has a golden test over that
output.

Every change then lands as exactly one of two things:

- **no golden diff**, which is what proves a change was a refactor
- **a deliberate regeneration**, whose diff is explained in the commit message

A diff that is neither is a change whose effect nobody has stated. Regenerating
goldens to make a build pass, without the explanation, discards the only record
of what the change did.

Adding an alternative to a shared structure is versioned and moves everything
together (POL-0063).

Golden tests require the output to be reproducible, which is why POL-0019 is
their precondition rather than a separate concern.

Structured output is too large to assert by hand and too small a change to
notice by eye, so without a golden there is no level at which a modification is
reviewable. The golden converts "I believe this refactor changed nothing" from
a claim into a diff, and it is the only mechanism here that catches an unintended
change whose shape nobody predicted. That is also why the explained-regeneration
half is not optional: an unexplained regeneration has the same diff as an
undetected defect.
