# Canonical corpus audit v1 — final report

## Result

The audit covers all 291 identities in the inventory: 248 policies, 29
decided-once standard entries, and 14 exemplars. Every identity has an affirmative
disposition. There are 227 `keep` and 64 `revise` results; no identity was split,
merged, or removed.

By layer:

| Layer | Keep | Revise | Total |
|---|---:|---:|---:|
| Policies | 206 | 42 | 248 |
| Decided-once standard | 18 | 11 | 29 |
| Exemplars | 3 | 11 | 14 |
| **Total** | **227** | **64** | **291** |

The highest recorded severities were 22 major findings, 42 minor findings, and
227 notes. Every finding is resolved in the audited corpus. No blocking, major,
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
- disconnecting a destroyed coroutine frame from its pending continuation;
- checking wire range before floating-point narrowing and documenting quantization;
- computing finite running means without an overflowing intermediate sum;
- enforcing finite window bounds and single-reader coroutine registration;
- distinguishing an allocation-free path from measured deadline compliance.

The resolved cross-corpus findings are recorded in `cross-slice.md`. Replacement
edges, topic membership, routing, standard grouping, and exemplar provenance remain
structurally valid after the changes.

## Evidence boundaries

Three different claims are kept separate:

1. **Deterministic validation.** `polc audit check --final`, the compiler tests,
   both projection modes for both stock configurations, compilation and execution
   of every exemplar's production and adjacent test translation units, C compilation of the shared driver
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

Brownfield normalization may proceed from this audited corpus version: the
verification commands in [integration-verification.md](integration-verification.md)
pass, including 55 Python tests, all 14 executable exemplar suites and the C11
header check, both deterministic evaluators, all four stock projections, and
matching independently built wheel and archive hashes. Target projects
still own their platform facts, exceptions, and deviations through overlays; this
audit does not turn canonical defaults into universal C++ law.


## Post-audit addition

POL-0249 was added after the original integration audit without topic membership
or an audit record. It now belongs to Writing a function, and the topics 1–5
report records its semantic review. The correction distinguishes optional NRVO
from guaranteed same-type prvalue initialization, narrows the restriction on
`std::move`, and avoids forcing construction through one mutable result. The
totals above include this addition; earlier slice reviews retain their provenance.

## Standard, FFI, and coroutine follow-up

Verification of issues #31, #33, and #34 found five further corrections: formatter
keys now enforce the declared layout; a C-string boundary contains exceptions;
FFI ownership distinguishes conversion, copy, move, borrowing, and explicit
transfer; fallthrough guidance admits C++14; and coroutine lifetime guidance
accounts for borrowed views and enforced referent lifetimes. EXM-0014 prose now
explains its ownership guarantee without asserting references always dangle.
All findings are resolved and recorded in the owning reports.

## Issue 36 integration follow-up

The complete-tree review retained every exemplar identity and demonstrates claim.
Additional numeric-boundary, reduction, waiter-registration, null-slot, and
deadline-scope findings are corrected in EXM-0006, EXM-0007, EXM-0009, EXM-0012,
and EXM-0014. These were already revised identities, so the disposition and
highest-severity totals remain unchanged. Runtime regressions and reproducible
commands are recorded in the integration verification document. No unresolved
cross-slice finding or new compiler invariant remains.
