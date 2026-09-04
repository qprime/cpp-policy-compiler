# Relay CAN experiment protocol

## Frozen inputs

- Target repository: `qprime/relay`
- Starting commit: `fe4fd63c1d87969d501296178051ffc0d7c474c8`
- Task: Relay issue #28, “Add deterministic CAN broadcast and arbitration as a
  third comm strategy,” as frozen on 2026-09-04
- Model family: Codex GPT-5
- Arms run sequentially in isolated Git worktrees

The issue body is the task prompt. Both generation arms receive the same issue
text and the same instruction: implement the issue completely, run every
required check, and commit the result. The baseline receives no compiled policy
projection. The treatment receives the full generation projection built from
this repository for Relay's C++23/GCC/realtime configuration.

## Generation arms

| Arm | Worktree | Additional context |
|---|---|---|
| baseline | `/home/squinlan/Code/relay-can-baseline` | Relay repository instructions only |
| generation-projection | `/home/squinlan/Code/relay-can-generation` | Same inputs plus the compiled generation projection |

For each arm, preserve the original state, the first coherent state at which the
agent claims implementation is complete, and the final state after its own test
and repair loop. Record the session event log, final response, commits, test
output, and diff. A state is not considered coherent merely because files were
quiet while the agent was still editing.

## Frozen generation oracle

The following requirements are fixed before either implementation begins:

1. All pre-existing Python and C++ tests pass.
2. The new CAN scenario passes in Python and the C++ host with good priorities.
3. Swapping only the two relevant CAN IDs produces the specified `PRECEDES`
   failure in both runtimes.
4. Python and C++ agree on CAN frame bit counts and deterministic delivery
   timing for the required golden vectors.
5. Generated ST publishes once per signal and contains no consumer PLC target.
6. A multi-consumer publication increments sequence once and reaches every
   declared consumer.
7. Validation rejects invalid baud, invalid or duplicate 11-bit IDs, duplicate
   consumers, self-consumption, and unknown PLCs on Python and host load paths.
8. Arbitration covers simultaneous readiness, non-preemption, idle-bus start,
   queued rounds, filters, repeated values, and scan-boundary completion.
9. PLC declaration order, frame declaration order, and coroutine scheduling do
   not change normalized traces or verdicts.
10. The third-strategy module extraction and transport registry contain no
    framework branch on the literal strategy name `can`.
11. Plant routes remain local and do not consume modeled CAN bandwidth.
12. Existing tag and address expectations reproduce; golden ST changes are
    limited to the intentional target-free publication migration.
13. Required trace metadata is present for CAN and older traces remain readable.
14. The affected invariant and protocol documentation matches the implementation.
15. Ruff, pyright, pytest, CMake build, CTest, expectation regeneration, and the
    repository's CI-equivalent checks pass.

Requirements 1–13 are correctness requirements. Requirement 14 is reviewed
manually for semantic agreement. Requirement 15 records tool outcomes without
claiming those tools prove requirements they do not check.

## Review experiment

Reviewers receive immutable, anonymized final snapshots and do not edit them.
Run these review contexts against the same snapshots:

1. baseline: repository instructions only;
2. generation projection: the same projection used while implementing;
3. review projection: a projection containing review-enforced rules, failure
   patterns, invariant-check procedure, and stable policy identities, without
   generation exemplars or implementation recipes that are irrelevant to review.

Before review, seed a separate copy with mechanically small defects selected
from the frozen requirements. Keep the unseeded implementation available to
measure false positives. Do not seed a defect until its expected path, line
range, policy identity, and observable consequence are recorded in the oracle.

Score review recall, precision, policy-citation accuracy, and actionability.
Adjudication uses tests, standards, and the frozen issue—not reviewer consensus.

## Integration rule

The experimental arms are evidence, not production branches. After scoring,
select the stronger base, apply only adjudicated corrections, rerun the complete
oracle, and land that corrected result on Relay's normal development branch.
Store experiment manifests, observations, and findings here; store only the
production implementation and its ordinary documentation in Relay.
