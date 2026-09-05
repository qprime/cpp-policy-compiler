# Canonical corpus audit v1 — final report

## Result

The audit covers all 290 identities in the inventory: 247 policies, 29
decided-once standard entries, and 14 exemplars. Every identity has an affirmative
disposition. There are 231 `keep` and 59 `revise` results; no identity was split,
merged, or removed.

By layer:

| Layer | Keep | Revise | Total |
|---|---:|---:|---:|
| Policies | 210 | 37 | 247 |
| Decided-once standard | 18 | 11 | 29 |
| Exemplars | 3 | 11 | 14 |
| **Total** | **231** | **59** | **290** |

The highest recorded severities were 18 major findings, 41 minor findings, and
231 notes. Every finding is resolved in the audited corpus. No blocking, major,
or accepted minor debt remains open.

## Review outcome

The revisions preserve all stable identities. They narrow universal claims,
correct C++ and FFI semantics, align the standard and policy layers, and repair
exemplar evidence. Material corrections include:

- distinguishing expected failure in return types from C++ exceptions;
- scoping determinism to an explicit reproducibility contract;
- making move `noexcept` specifications conditional and truthful;
- correcting pointer relational comparison, signed arithmetic, templates, and
  coroutine-lambda lifetime guidance;
- treating public C ABI entry points as trust boundaries and keeping C source
  under a C compiler;
- redacting unsafe diagnostic values and allowing explicit cross-language naming
  maps;
- rejecting non-finite temperatures throughout copied exemplar source;
- disconnecting a destroyed coroutine frame from its pending continuation.

The resolved cross-corpus findings are recorded in `cross-slice.md`. Replacement
edges, topic membership, routing, standard grouping, and exemplar provenance remain
structurally valid after the changes.

## Evidence boundaries

Three different claims are kept separate:

1. **Deterministic validation.** `polc audit check --final`, the compiler tests,
   both projection modes for both stock configurations, syntax compilation of
   exemplar production translation units, C compilation of the shared driver
   header, evaluator fixtures, and reproducible installed release archives check
   structure and executable invariants.
2. **Expert semantic review.** The slice reports record the technical, strength,
   scope, routing, consistency, attribution, example, and model-readability
   judgment for every identity. Passing tools do not substitute for these rows.
3. **Measured model behavior.** No paid or nondeterministic live-model trial was
   run. The existing checked-in benchmark remains historical integration evidence,
   not proof that every audited rule changes model behavior or is universally
   correct.

No new behavioral uncertainty discovered here justified a live-model benchmark
issue. Future wording changes that claim an effectiveness improvement should state
a focused hypothesis and use the opt-in evaluator rather than adding model calls to
normal builds.

## Completion gate

Brownfield normalization may proceed from this audited corpus version once the
verification commands recorded with the integration commit pass. Target projects
still own their platform facts, exceptions, and deviations through overlays; this
audit does not turn canonical defaults into universal C++ law.

