# Relay CAN experiment results

Run on 2026-09-04 from Relay `fe4fd63c1d87969d501296178051ffc0d7c474c8`
with Codex `gpt-5.6-sol` at the same reasoning setting in both arms.

## Generation

| Arm | Relay commit | Tokens | Elapsed | Recorded states | Final Python suite |
|---|---:|---:|---:|---:|---:|
| repository-only | `26142a6` | 263,865 | 30m 26s | 143 | 614 passed |
| generation projection | `60a974a` | 242,147 | 26m 17s | 120 | 616 passed |

Both generated commits built warning-clean, passed CTest, Ruff, and Pyright, and
produced the intended good/pass and swapped-priority/fail scenario. These green
checks did not make the implementations equally correct.

Blinded review ranked the repository-only implementation (snapshot A) above the
generation-projection implementation (snapshot B) in all three review contexts.
B had confirmed non-preemption/exact-boundary scheduling defects, incomplete
host-load validation, Python/C++ Boolean handling divergence, and incomplete C++
trace validation. A was selected as the production base. Its confirmed review
findings included partial trace-metadata acceptance, unsafe delayed writes into
a wrapping trace ring, transport-selection/documentation drift, and later two
host scheduler/interleaving defects.

The important result is not “the projection won.” It did not. It used 8% fewer
tokens and 14% less elapsed time, but produced the weaker implementation. This
single task is evidence about this projection, not a general model-quality claim.

## Seeded review

The corrected A snapshot was copied to C. Snapshot D differed only by swapping
the critical/background IDs in `can_contention_good.yaml`; the seed was frozen in
`SEEDED_ORACLE.md` before review.

| Review context | Clean C findings | Seeded D findings | Seed found | Additional findings adjudicated real |
|---|---:|---:|---:|---:|
| repository-only | 0 | 1 | yes | 0 |
| generation projection | 1 | 2 | yes | 1 |
| review projection | 2 | 3 | yes | 2 |

All contexts therefore had 100% recall on the seeded bad priority and no
unsupported finding. If precision is computed mechanically against only the one
seed label, the richer reviews look less precise because they found real defects
that the frozen seed oracle did not list. Adjudicated precision is 100% for all
three; report-level seed-only precision is 100%, 33%, and 20% respectively.

The review projection added material value: it alone found that a faster PLC
could settle the shared bus into the future and expose a completed frame to a
slower consumer before that consumer's logical clock reached completion. Both
policy-aware reviews found that a poll interleaved between same-time producer
emits could start arbitration before all contenders were present.

## Production result

The stronger base plus adjudicated corrections is Relay `83ad8ff` on `master`:

- `fecb123` — generated CAN implementation;
- `799ac70` — first blinded-review corrections;
- `83ad8ff` — scheduler/interleaving corrections and focused C++ tests.

Final verification: expectation regeneration stable; 616 Python tests; Ruff;
Pyright; warning-clean C++ build; 145 C++ tests. The experiment artifacts live
here, while Relay contains only the production implementation and its ordinary
tests/docs.

## Harness observation

The recorder captured every quiet filesystem state under `host/`, including the
CMake build tree. That made 263 source trajectories consume about 59 GB and did
not identify the first coherent completion claim. Raw state directories were
therefore treated as disposable run data after extracting counts, timings,
responses, commits, findings, and reproducible snapshots. A follow-up harness
change should exclude ignored/build artifacts and accept an explicit coherent
checkpoint marker; filesystem quiet is not a semantic checkpoint.
