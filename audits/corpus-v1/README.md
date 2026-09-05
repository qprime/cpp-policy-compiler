# Canonical corpus audit v1

This directory records the semantic audit governed by issue #28. Structural
validation proves that the corpus can be parsed and projected; it does not prove
that the engineering advice is true.

Run the incremental coverage check from the repository root:

```text
polc audit check --root audits/corpus-v1
```

Add `--final` only at the integration gate. Incremental checks accept reports
whose whole slice is explicitly `pending`; final checks reject every pending
slice and every unresolved blocking or major finding.

## Rubric

Each identity must answer all ten questions:

1. `technical_truth`: Is the advice correct for every admitted C++ version,
   compiler, domain, lifetime, concurrency, ABI, and tooling assumption?
2. `strength`: Does its normative strength match how universal the decision is?
3. `scope`: Does applicability exclude contexts where it is unavailable,
   vacuous, or harmful without specializing the canonical corpus to one project?
4. `decision_clarity`: Does it give an operational decision and legitimate
   exception rather than taste or an undefined “best practice”?
5. `generation_routing`: Does the trigger describe the authoring situation?
6. `review_routing`: Does the review trigger describe observable evidence, or
   explicitly record why reliable review routing is unavailable?
7. `consistency`: Does it avoid conflict or unexplained overlap with principles,
   peers, standards, overlays, and version mechanisms?
8. `attribution`: Does every checked locator exist and support the rule's actual
   scope and strength, with corpus-original judgment labeled honestly?
9. `examples_and_evidence`: Are examples conceptually valid, free of adjacent
   defects, and consistent with every exemplar claim?
10. `model_behavior`: Is the wording resistant to misreading, cargo culting, and
    mechanical application outside its scope?

A dimension is `reviewed`, `finding`, or `not-applicable`. The latter two require
a concise reason. A reviewer's agreement is not evidence by itself; blocking
technical claims use captured source or primary specifications.

## Vocabulary

Severities are `blocking` (unsafe or invalidates the audit), `major` (materially
wrong or misleading), `minor` (bounded debt), and `note` (no correction needed).

Dispositions are `keep`, `revise`, `split`, `merge`, and `remove`. `keep` is an
affirmative result, not an omitted row. A non-keep result names either a completed
change with repository-relative files and commit, or an unresolved follow-up
issue. Stable identities remain stable unless the underlying decision truly
splits, merges, or disappears.

## Reports

`inventory.json` is generated from parsed policy identities, topic membership,
standard entries, and exemplars. Do not hand-edit ownership. Reports become
`complete` only when they contain every owned identity, in inventory order, with
this shape:

```json
{
  "id": "POL-0001",
  "disposition": "keep",
  "dimensions": {
    "technical_truth": {"status": "reviewed"}
  },
  "highest_severity": "note",
  "rationale": "Concise affirmative audit conclusion.",
  "evidence": ["docs/source/..."],
  "related_ids": [],
  "change": null,
  "follow_up_issue": null,
  "finding_status": "resolved"
}
```

The real record contains all ten dimensions. Cross-slice findings go in
`cross-slice.md`; do not silently edit an identity owned by another report.

