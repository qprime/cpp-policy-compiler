---
description: Deletion pass on a settled document. Removes conversational residue and generator artifacts, keeps what someone working from the doc needs. Pure excision — never rewrites. Use when a doc has stopped being a conversation artifact and become a reference.
---

# /clean-slop — Deletion Pass

Run a deletion pass on: $ARGUMENTS

A document written across a long conversation accumulates sentences that were
load-bearing when someone wrote them and are not anymore. Delete them. Do not
rewrite.

## Fix the Counterfactual

Before you cut anything, state the question every cut has to answer: what would a
reader do differently without this sentence? Build something else, take a
different action, write different code, reopen a decision.

## Load the Constraints

You can annoy a reader by leaving residue. You cannot get back a fact you cut.
Find out what the document has to keep before you start.

Look for a constraints block at the top of the file:

```
<!-- clean-slop: preserve component numbering, the pipeline diagram's column
     alignment, every fact marked verified. -->
```

Where you find none, derive the constraints from the file, state them, and get
confirmation before you cut.

Never cut these, whatever the constraints say: verified facts, identifiers and
numbering, table and diagram alignment, code blocks, and anything a reader could
not reconstruct from the codebase.

## How to Cut

**Excise, never paraphrase.** Keep the diff all red, so a reviewer reads only what
left. Where a fact sits inside a sentence you would otherwise cut, leave the
sentence whole and note it in the report.

**Test claims, not sentences.** Three sentences can carry a claim together when no
single one of them changes the answer to the counterfactual. Cut the claim or keep
it.

**Strand nothing.** Never leave a statement pointing at a referent you removed.

**Leave the gaps.** Write no transitions to smooth them over.

**Relocate rather than delete.** Where content fails the test here but would pass
it in another document, flag it and name the destination. Name a destination only
where the project has that file. Leave the content in place and let the user move
it.

**Do not reopen a design decision.** Where one looks wrong, say so and leave it.

## Report

- What you removed, by category
- Any sentence you left standing because a fact sat inside it
- Anything you flagged for relocation, with its destination
- Any constraint you inferred rather than read
- Any decision that looked wrong and you left alone
