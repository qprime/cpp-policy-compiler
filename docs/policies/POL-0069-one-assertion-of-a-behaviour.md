---
id: POL-0069
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Testing: one assertion of a behaviour"
---

# One assertion of a behaviour

Two tests covering the same behaviour over the same input are a defect, not
redundancy. Before adding a test, find whether the behaviour is already
asserted; before adding a test file, find whether one exists for the unit.

Coverage is a question about behaviours, not about test count. A second test of
a covered behaviour raises the count and covers nothing.

The duplicate does not stay a duplicate. One copy gets updated when the
behaviour changes and the other does not, which leaves a suite asserting two
contradictory things about one input; whichever fails first is treated as the
broken one, and there is no way to tell from the tests which was right.
Duplicates also cost every future change twice, so the suite gets slower to
maintain in proportion to how thoroughly it was duplicated. The cost falls
hardest on generated tests, which are written from the code rather than from a
list of what is already asserted.
