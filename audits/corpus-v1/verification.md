# Verification of corpus audit issues 29–35

The requested implementations were already present upstream when this checkout
was updated. Their original commits and reports remain the evidence for the
completed semantic reviews; this verification does not claim to repeat every
earlier technical review.

| Issue | Existing implementation | Current report coverage |
|---|---|---|
| #29 | `fd55438`, deterministic audit framework | 248 policies, 29 standard entries, 14 exemplars |
| #30 | `378174c`, principles and anti-patterns | 20 complete records |
| #31 | `3e5e34c`, decided-once coding standard | 29 complete records |
| #32 | `e5eea97`, topics 1–5 | 122 complete records, including the subsequent POL-0249 review |
| #33 | `015c621`, topics 6–10 | 36 complete records |
| #34 | `d127f6d`, topics 11–15 | 26 complete records |
| #35 | `facd2f6`, topics 16–20 | 44 complete records |

The later `7e991c2` addition introduced POL-0249 without topic membership or an
audit record. That omission prevented projections and audit validation from
running. This change assigns it to Writing a function, regenerates the inventory,
records its primary-source semantic review, and corrects its return-value claims.
The audit regression tests now also exercise live identity addition, removal,
and duplicate topic membership. The inventory count and review routing expectation
include the new policy.

## Follow-up for issues 31, 33, and 34

The existing content and reports were checked against these issues' acceptance
criteria. Five corrections were made with primary-source evidence recorded in the
owning slice reports:

- STD-0027 now disables derived pointer alignment and sets the access modifier
  offset to -3, so its four-space Google-based configuration actually enforces
  left-aligned pointers and one-space access labels. The old and corrected
  configurations were exercised with clang-format 18.1.3.
- POL-0043 now contains string-construction and operation exceptions inside its
  public C boundary, names the readable null-termination contract, and distinguishes
  C++14 from standard string-view availability.
- POL-0237 distinguishes conversion, copying, moving, borrowing, and explicitly
  contracted ownership transfer rather than treating all value crossings as copies.
- POL-0144 distinguishes C++17 standard fallthrough markers from C++14 diagnostic
  mechanisms, and permits stacked case labels without a marker.
- POL-0179 describes the referent lifetime needed across suspension and cancellation,
  including the borrowing risk of pointers and views passed by value. EXM-0014 prose
  now explains its owning shared-pointer guarantee without claiming references
  inherently dangle; the cross-slice ledger records that correction.

EXM-0008's jumping switch arms and EXM-0013's boundary conversions remain valid
demonstrations. EXM-0014's production coroutine source passes C++20 syntax
compilation. No exemplar evidence identities were transferred or relabeled.

## Validation

The full `uv run pytest -q` suite passes: 55 tests, including deterministic
evaluator fixtures and installed-distribution checks. Both incremental and final
audit coverage checks pass:

```text
uv run polc audit check --root audits/corpus-v1
uv run polc audit check --root audits/corpus-v1 --final
```

Both `cpp20-gcc-application` and `cpp23-gcc-realtime` pass `polc check` in
generation and review modes. Two independently built wheels were installed and
used outside the checkout to produce their stock archives. The wheel and both
stock archives match byte-for-byte across builds. `git diff --check` passes.

The corrected C-boundary fragment was compiled and executed with success,
ordinary failure, null input, and thrown-exception inputs under C++14, C++20,
and C++23. Rendered standard, setup, FFI, statement, and coroutine documents
were checked in all four stock projections. CMake and Catch2 remain the canonical
setup choices, and the corrections introduce no configuration fields or schema
changes.

These checks establish structural validity and reproducibility. The earlier
slice reports and POL-0249's new review supply semantic judgments. No live-model
trial was run, and passing checks do not establish model effectiveness. Missing
entry-level review routes continue to be reported by the compiler; this change
does not invent routes for the rest of the corpus.
