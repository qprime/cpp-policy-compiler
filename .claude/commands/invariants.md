---
layer: global
description: Extract, review, and maintain load-bearing project invariants from code, tests, docs, and git history.
argument-hint: [extract | commit | audit | check <path>]
---

# /invariants

Extract, review, and maintain this project's load-bearing invariants. Output lives in `docs/invariants/`. The command owns its own setup and writes only there. This directory is project-authored content — no tooling generates it.

---

## Definition

**Invariants are load-bearing rules. Violating them breaks the system.**

The contrast that matters:

- **Invariant** — violating it breaks correctness. The system stops working, or works wrong in ways that compound.
- **Convention** — violating it creates drift, friction, or noise. The system still works; reviewers and agents diverge.

Style preferences are conventions. Performance targets are SLOs. Security policies are separate. Aspirations are unenforced claims. None of those are invariants.

If a candidate would still let the system work after being violated, it is not an invariant. Drop it or move it to conventions.

Type classifications below describe *kinds* of invariants; they do not redefine what an invariant is.

### Type taxonomy

- `HARD` — violation breaks the system.
- `STRUCTURAL` — changeable only via coordinated migration across multiple files.
- `POLICY` — current default; can change with care.
- `FALLBACK` — defensive code; firing means an upstream bug.
- `SAFETY` (orthogonal flag) — violations corrupt data, damage hardware, or harm users. Hard-error only; never warn-and-continue.

For ambiguous classifications, prefer the weaker type (POLICY over STRUCTURAL, STRUCTURAL over HARD) and flag for user review during `commit`.

---

## Subcommands

Dispatch on the first argument:

- `extract` — read the project, emit `docs/invariants/candidates.md`. Never edits authoritative invariant files.
- `commit` — interactive review of candidates within this Claude Code session, then atomic write of structured invariant docs.
- `audit` — drift check; verify each invariant's evidence still exists; emit a dated audit report; never modify invariant files.
- `check <path>` — given a file or diff path, list every invariant whose evidence or scope references it. Read-only.

If no argument is given, print this command's purpose and the four subcommands, then stop.

---

## First-run setup

On any subcommand invocation, before doing the subcommand's work:

1. If `docs/invariants/` does not exist, create it.
2. If `docs/invariants/README.md` does not exist, write a placeholder index:

   ```markdown
   # Invariants

   No invariants recorded yet. Run `/invariants extract` to surface candidates from code, tests, docs, and git history; then `/invariants commit` to review and write authoritative subsystem files.

   Subsystem files: none yet.
   ```

3. If the project's `CLAUDE.md` exists and contains no line referencing `docs/invariants/` or `/invariants`, add a one-line pointer to its look-up map section, of the form:

   > Invariants live at `docs/invariants/`; maintained by `/invariants`.

   Idempotent: if any line already references `docs/invariants/` or `/invariants`, leave `CLAUDE.md` alone. If `CLAUDE.md` does not exist, do not create one — the pointer is added the next time `CLAUDE.md` itself is.

4. Do not touch `README.md`.

`docs/invariants/` is a hardcoded path. Do not read it from configuration and do not honor a different one.

---

## `extract`

Read the project. Surface candidate invariants under `docs/invariants/candidates.md`. Never write to authoritative subsystem files.

### Evidence threshold

A candidate surfaces only when at least one of these is present:

- A runtime assertion, validator, or `raise` enforcing the rule.
- A negative test (asserts the violation is rejected).
- A type-system constraint (`Final`, frozen dataclass, `NewType`, exhaustive match).
- A CI gate, lint rule, or pre-commit hook enforcing it.
- A historical bug fix or revert that re-asserted it (regression-trap detection, below).
- An explicit prose assertion in `README.md`, `CLAUDE.md`, an ADR, or `docs/` — only paired with one of the above. Prose alone does not qualify.

Aspirational rules in prose without enforcement go under a separate `## Unenforced Claims` section in `candidates.md`. They do not become candidates.

### Regression-trap detection

Mine git history for:

- Commits with subjects matching `revert|restore|put back|undo|re-add|bring back` (case-insensitive).
- Files where the same lines were changed and reverted within 90 days.
- Code comments matching `do not (refactor|remove|simplify|inline)`, `looks (redundant|unused|wrong) but`, `keep this`, `intentional`, `do not touch`, `here be dragons`.
- Pull-request descriptions or commit bodies referencing prior breakage of the same invariant.

Candidates surfaced this way carry `regression_trap: true` and a `Why (inferred)` line drawn from the relevant commit message.

If git history is shallow, run regression-trap detection against whatever history is available and report the depth in the candidates output.

### ID convention (suggested in extract; finalized in commit)

- Two-letter subsystem prefix + monotonic number: `PL-1`, `PL-2`, `DS-1`, `CT-3`.
- Numbering preserves gaps on retirement: `~~EV-3~~ deferred`, `~~SG-1~~ retired`.
- Name: SCREAMING_SNAKE_CASE, e.g. `IR_LAYER_REQUIRED`, `NO_DOMAIN_MUTATION`.
- Header form: `## PL-2: IR_LAYER_REQUIRED (HARD)` or `## EV-4: CALIBRATOR_IS_FITTED_ARTIFACT (HARD, REGRESSION TRAP)`.

`extract` may suggest IDs but treats them as drafts; `commit` finalizes them when subsystem files are written.

### Candidate output format

Each candidate is a YAML block in `candidates.md`:

```yaml
- id_suggested: PL-3
  subsystem: pipeline
  type_suggested: HARD
  safety_critical: false
  regression_trap: false
  rule: >
    One-line statement of the contract.
  why_inferred: >
    Drafted from <source>. NEEDS USER CONFIRMATION.
  evidence:
    - kind: assertion
      path: src/pipeline/runner.py:142
      excerpt: "assert ir is not None, 'IR layer required'"
    - kind: negative_test
      path: tests/test_pipeline.py::test_rejects_missing_ir
    - kind: history
      ref: a1b2c3d
      note: "reverted 'simplify pipeline' commit"
  example_required: true
  example_wrong: |
    runner.execute(raw_input)
  example_correct: |
    runner.execute(IR.from_raw(raw_input))
  scope_notes: >
    Does not apply to compositional.py or diagram_ir/shapes.py.
  confidence: high
```

Required fields: `rule`, `evidence` (≥1 entry), `confidence`. All `why_*` fields are explicitly marked `_inferred` and need confirmation in `commit`. Never assert a why as if it were extracted from the code.

### `example_required` decision

Per-candidate. Syntactic / API-shape rules → `true`; the example is load-bearing. Architectural rules (determinism, immutability across the board, pipeline ordering) → `false`; a snippet trivializes them. Decide per-candidate and explain the choice in a `# note:` comment when `false`.

### Output structure

```markdown
# Invariant candidates — extracted <date>

History depth: <depth note, if shallow>

## Candidates

<YAML blocks per candidate>

## Unenforced Claims

<prose-only claims found in docs without code-side enforcement>
```

If zero candidates pass the threshold, emit the file with an empty `## Candidates` section and the `## Unenforced Claims` section populated (if any). Report explicitly that no enforced rules were found.

### Re-extraction

If `candidates.md` already exists, overwrite it. The user is expected to commit or discard a previous candidates file before re-running extract.

---

## `commit`

Interactive review of `docs/invariants/candidates.md` within this Claude Code session. Atomic write of structured invariant docs at the end.

If `candidates.md` does not exist, report "no candidates to commit" and stop.

For each candidate:

1. Present rule, evidence, inferred why, suggested type, confidence.
2. Prompt the user for one of: accept / reject / edit / skip / type-change / why-rewrite.
3. On accept, assign the final ID — subsystem-prefixed, monotonic with gaps preserved across retirements — and stage the candidate for write.

After all candidates are reviewed:

1. Atomically write or update each affected `docs/invariants/<subsystem>.md`.
2. Atomically write or update `docs/invariants/README.md` (the index).
3. Move `candidates.md` to `candidates.archived-<date>.md`, or delete it, per user choice.

### Authoritative subsystem-file format

```markdown
# Invariants — <subsystem>

| ID | Type | Safety | Invariant |
|----|------|--------|-----------|
| PL-1 | HARD |  | IR layer required for all pipeline entry. |
| PL-2 | STRUCTURAL | SAFETY | Tool clearance verified post-generation. |

## PL-1: IR_LAYER_REQUIRED (HARD)

**Why:** RemovalIntent is the semantic validation layer. Bypassing it means no validation, no extensibility.

**Scope:** All pipeline entry points. Does not apply to compositional.py.

**Regression trap:** Yes — historical commits a1b2c3d, e4f5g6h reverted attempted bypasses.

**Wrong:**
```python
runner.execute(raw_input)
```

**Correct:**
```python
runner.execute(IR.from_raw(raw_input))
```

**Evidence:**
- assertion: `src/pipeline/runner.py:142`
- negative test: `tests/test_pipeline.py::test_rejects_missing_ir`
```

Each subsystem file leads with the type-table summarizing all IDs in the file.

### README index format

```markdown
# Invariants

Subsystem files:

- `pipeline.md` — PL-1, PL-2, PL-3
- `data-store.md` — DS-1, DS-2

Global axioms (rules that span subsystems): listed at the top of the relevant subsystem file with cross-references.

Regression traps: marked inline on each invariant header.

Error philosophy: <one-line policy on hard-error vs warn-and-continue, if the project has one>.
```

---

## `audit`

Drift check. Never modifies invariant files.

For each invariant in the README index and subsystem files:

- Verify each `evidence` entry's path/line still exists. Allow fuzzy match within ±3 lines for line-numbered references.
- Re-run regression-trap heuristics against git history since the last audit; flag new traps.
- Flag invariants whose evidence has weakened: assertion removed, test deleted, comment changed.

Emit `docs/invariants/audit-<date>.md` (append-only — do not overwrite prior audits):

```markdown
# Invariant audit — <date>

## Summary

<count> invariants checked. <count> evidence-intact. <count> weakened. <count> new regression traps surfaced.

## Weakened

- **PL-2** — evidence `src/pipeline/runner.py:142` no longer present (assertion removed in commit a1b2c3d). Recommend: re-extract for this subsystem.

## New regression traps

- **DS-1** — commit e4f5g6h reverted "simplify storage layer", which corresponds to DS-1's rule. Mark DS-1 with `REGRESSION TRAP` on next commit.
```

Do not modify invariant files. Recommendations only.

---

## `check <path>`

Given a file or diff path, list every invariant whose evidence or stated scope references that path. Read-only.

Output groups invariants by severity:

- `must-not-violate` — HARD, SAFETY
- `coordinate-migration` — STRUCTURAL
- `consider` — POLICY, FALLBACK

Format per invariant: `<ID>: <one-line rule> (<type>) — why: <one-line>`.

If no invariant references the path, print "no invariants reference this path" and stop.

---

## Constraints on this command

- The command owns `docs/invariants/`. No other tooling generates, validates, or writes under it.
- The command runs inside the project; subcommands depend on reading project code, tests, docs, and git history.
- The command never invents enforcement — every candidate must trace to evidence above the threshold.
- The command never asserts a why as extracted; whys are inferred and marked for confirmation.
- The command never modifies invariant files outside the explicit `commit` step.
