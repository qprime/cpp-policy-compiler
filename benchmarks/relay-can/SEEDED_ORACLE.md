# Seeded review oracle

Frozen before the seeded review runs on 2026-09-04.

- Unseeded snapshot: `/tmp/relay-can-review-c` at Relay commit `6b6e05e`.
- Seeded snapshot: `/tmp/relay-can-review-d`, identical except lines 12–13 of
  `specs/can_contention_good.yaml` swap CAN IDs `0x080` and `0x300`.
- Stable identity: Relay issue #28 priority rule; lower 11-bit CAN ID wins.
- Observable consequence: the file named and expected as the good scenario now
  gives the critical publication lower priority, crossing the 30 ms `PRECEDES`
  budget and contradicting its checked-in expectation artifact.
- Expected actionable finding: exactly this priority/expectation mismatch.

Review recall is 1 when this finding is reported for D and 0 otherwise. Any
other reported defect on unchanged C or D is adjudicated separately and counts
against precision if unsupported. Reviewers do not receive this oracle.
