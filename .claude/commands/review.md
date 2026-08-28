---
description: Code and architectural reviewer for inspecting quality, correctness, and invariant compliance. Use when the user asks for a code review. Accepts an issue reference, file paths, spec text, or the working diff. Read-only — does not modify code.
---

# /review

**AI hazards** are patterns that mislead an agent reading the code cold: dead
types, misleading names, stale comments, shapes that invite the wrong pattern, or
structure that reads as one thing and behaves as another. Flag these explicitly.

## Context

Read `CLAUDE.md` and follow its Look-Up Map to the invariants, the conventions,
and any prior review context. Identify which invariants govern the files in scope
before you start.

## Scope

Review what the user names: a spec, the working diff, file paths, an issue. For an
issue, find the associated commits or PR through the issue tracker first.

**No arguments: ask.** Never pick a scope on your own.

Read every file under review in full, not just the changed lines. Cross-reference
against the invariants and the downstream consumers.

## What to Look For

Beyond correctness and coverage, which you check by default:

- **AI hazards** — patterns that cause agent mistakes
- **Invariant compliance**
- **Structural problems** — duplication, layer violations, broken boundaries
- **System impact** — downstream effects
- **Convention drift** — read the conventions before you flag a pattern

## Triage

Give every finding exactly one disposition:

| Disposition | Criteria | Report under |
|---|---|---|
| **Fix now** | Invariant violation, crash path, data loss, silent failure, AI hazard, or any footgun you can fix inline | File These |
| **File an issue** | Real problem whose footprint is too large to fix inline, or scope this spec does not cover | New Issues |
| **Ignore** | Valid observation carrying no risk, or a problem that surfaces naturally at the point of use | Noted, Not Actionable |

Give each Ignore one line on why it is safe to ignore.

## Report

Omit a section that does not apply. Invariant Compliance and System Impact apply
to code. Proposed Spec Edits applies to specs.

```
## Review Scope
- Trigger: [what you were asked to review]
- Artifact type: implemented code / spec
- Context loaded: [what you read]
- Files reviewed: N reviewed, N skipped

## File These
- **[defect]** description — `file:line` — violates [invariant ID / convention]
- **[AI hazard]** description — `file:line` — causes [specific agent mistake]

## New Issues
- description — `file:line` — too large to fix inline

## Noted, Not Actionable
- observation — why it is safe to ignore

## Potential Conventions
- Undocumented but consistent pattern observed: [description]. Consider codifying.

## Invariant Compliance
| Invariant | Status |
|-----------|--------|
| XX-N (NAME) | Compliant / Violation |

## System Impact
- downstream effect

## Checks Performed
- [what you actively looked for — invariant scan, cross-file mutation check,
  import-layer traversal, requirement contradictions, adjacent-issue overlap]

## Verdict
"**Clean**" or "**N issues** — M bugs, K architectural concerns"

## Proposed Spec Edits
[exact edits, for user approval]
```

## Report to the Issue

Where the review is tied to a GitHub issue, post the report to it with
`gh issue comment` as well as to the chat. Post without asking. Open the comment
with `**/review**` so the ticket reads as a conversation.

Post File These, New Issues, Noted Not Actionable, Invariant Compliance, and the
Verdict. Leave out Review Scope and Checks Performed — those are for the user
reading the session.

Where the review covers a local diff or file paths with no issue behind it, report
to the chat only.

## When Review Leads to Changes

Don't apply them. Report the findings and stop. Where the user asks for fixes,
that is `/engineer` for code and `/spec` for spec edits.
