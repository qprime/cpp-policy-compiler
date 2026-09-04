# Initial Correctness Findings

The first vertical experiment ran Claude Sonnet 5 once per variant on 2026-09-04.
It establishes that the benchmark can distinguish generation, convergence,
review recall, review precision, citation accuracy, and actionability. One run on
one small fixture is not an estimate of general model performance.

## Generation

The baseline and full generation projection both produced compliant first writes
for the two seeded rules. Both remained compliant at completion, so neither run
needed repair.

| Variant | First write | Final | Repair delta |
|---|---:|---:|---:|
| Baseline | 100% | 100% | 0 |
| Full generation projection | 100% | 100% | 0 |

This case proves the capture and comparison path but does not distinguish the
harnesses. Broader tasks and repeated runs are required before making a claim
about generation effectiveness.

## Review

The review fixture contains three defects and one clean function. The baseline
found all three defects but could not cite corpus identities. The generation
projection found the return and null-pointer defects, missed the unknown callback
under a lock, and mentioned the correct policy ids only inside evidence while
returning `F1` and `F2` in the required identity field.

| Variant | Recall | Precision | Citation accuracy | Actionability |
|---|---:|---:|---:|---:|
| Baseline | 100% | 100% | 0% | 100% |
| Generation projection | 67% | 100% | 0% | 100% |

The result justifies testing a separate review projection. Reusing generation
routing did not improve recall, did not produce machine-usable citations, and
failed to route the reviewer to the concurrency rule that directly governed the
third defect. The next experiment should compile review-specific procedure and
routing without duplicating policy identity or content.

## Limits

The findings are observations, not a benchmark conclusion. The task is small,
the sample count is one, and model behavior varies. The checked-in observations
remain useful as a reproducible evaluator fixture; claims about harness quality
require more tasks, repeated paired runs, and blinded adjudication for semantic
requirements.
