# Correctness Benchmarks

These benchmarks measure `polc`; normal projects do not run them. `polc build`
and `polc check` never record source files, repeat model tasks, seed defects, or
score agent output.

[Initial findings](FINDINGS.md) records the first live paired runs. Complete
machine results are regenerated from the checked-in manifests and observations.

Run a recorded benchmark explicitly:

```text
polc eval run benchmarks/generation/first-write.yaml --out result.json
polc eval run benchmarks/review/seeded-defects.yaml --out result.json
```

Record coherent versions of selected files while another command runs:

```text
polc eval record \
  --root ../target-project \
  --path src/sample.cpp \
  --out recording \
  --quiet-period-ms 500 \
  -- claude -p "Implement the requested change"
```

## Manifest

A version 1 generation manifest declares requirements and at least two states per
harness variant. `prompt` and `watched_paths` preserve the task and observable
boundary. Text checks use Python regular expressions. Command checks are argument
lists, run without a shell from the state root. `T1` is the second declared state
and the final state is the last.

A review manifest declares an oracle under `expected_findings` and one JSON
findings file per variant. A finding matches an oracle location by path and by
`line`, or the inclusive `line` to `line_end` range. The stable id is scored
separately as citation accuracy. Non-empty evidence makes a match actionable.
Clean constructs need no special record: any finding outside the oracle is a
false positive.

Results preserve individual requirement and finding outcomes. Compilation,
tests, formatters, and static analysis prove only the requirements their manifest
entries name; an absent diagnostic is never reported as universal compliance.
Use a `manual` check for a requirement that needs blinded adjudication; it renders
as `not-judged` and is excluded from compliance arithmetic.

## Recording

The recorder observes only the relative paths named on the command line. It
stores each distinct combined content hash once after the configured quiet
period and records the final hash even when the final content repeats an earlier
state. Raw filesystem events are not correctness evidence.
