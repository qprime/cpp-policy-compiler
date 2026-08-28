---
description: Draft a GitHub issue implementation specification. Use when planning a new feature, refactor, or bug fix that needs a detailed spec before implementation.
---

# /spec — Implementation Specification

Draft a GitHub issue implementation specification for: $ARGUMENTS

## Process

1. **Research first.** Before drafting, read: (a) every file named in the feature request, (b) the implementation files of any named subsystem, (c) `CLAUDE.md` and whatever its Look-Up Map points to for the affected code paths, and (d) existing tests covering those paths. List what you read in a short "Context loaded" block before drafting.

2. **Draft the spec** using the section template below. Write the sections in order. Omit an optional section when it does not apply.

3. **Check for a smaller change.** Before finalizing, ask: could a narrower scope — fewer files, fewer moving parts, less ceremony — achieve the same goal? If yes, redraft around that. Spec size should match change size. This is about scope, not about removing structure that serves invariants, type safety, or tests.

4. **Resolve, don't flag.** Settle every uncertainty before you draft: verify it against the code, cut the claim, or narrow the spec so it no longer rests on the guess. Where a question gates the draft and only the user can answer it, ask before you draft — never after.

   IMPORTANT: your message ends with the last section of the spec. No closing summary, no questions, no caveats, no next steps.

5. **Present the draft** in the chat and stop. Create the issue only when the user
   tells you to, then report the number. Never run `gh issue create` off an
   approval you inferred — the user often wants to work the draft locally first.

---

## Title

Start with an action verb. Describe what the change *does*, not what's missing or broken.

- **Good:** "Add drift detection for baseline version comparisons"
- **Bad:** "Projects don't know when their baseline is stale"

## Section Template

### Summary
1-3 sentences. What is being added, changed, or fixed. Actionable and specific.

### Motivation
Why this matters. Concrete pain points — user-facing or developer-facing. Not hypothetical benefits.

### Existing Architecture
What exists today that this change touches. Reference specific files and line numbers. Include function signatures, data flow, and relevant patterns.

### Design
The technical approach:
- **Data flow**: How data moves through the system. Use an ASCII diagram only if the shape isn't obvious from prose.
- **Code signatures**: Exact dataclass fields, function signatures with type annotations
- **Invariant impact**: Which invariants does this touch? Note here if any are bent; full compliance statement goes in the Invariants section below.

### Constraint Interactions
How this feature interacts with existing features. For each relevant interaction:
- Is it compatible, mutually exclusive, or conditionally compatible?
- What validation enforces the constraint?

*Optional — omit only if the change is truly isolated (rare).*

### Implementation
Phased or numbered steps. For each step:
- Which file(s) change
- What specifically changes (field additions, new functions, modified logic)

Use a per-file change table when touching 3+ files:

| File | Change |
|------|--------|
| `path/to/file` | Description of change |

### Invariants
Which invariants apply to this change. For each:
- Invariant ID and name
- Whether this change complies or requires a documented exception

### Edge Cases
Scenarios worth calling out and the expected behavior. Cover what's actually at risk for this change — missing/None inputs where relevant, adjacent work having or not having landed, analysis surfacing something unexpected, partial or conflicting state.

### Testing Strategy
Named test cases with expected behavior:

```
TestClassName:
    test_case_name — description of what it verifies
```

Include at least one test whose failure would catch a plausible wrong implementation — not just one that passes when the code is correct.

### What NOT to do
Anti-patterns and scope boundaries that aren't obvious from the positive rules above. Each bullet must earn its place by meeting at least one of:
- Prevents a failure mode that actually happened in a prior issue/review
- Non-obvious from the Design / Implementation sections (a reader would not infer it)
- Draws a scope boundary against adjacent work (other open issues, sibling subsystems)

If a bullet just restates a rule already given positively, cut it. Omit the whole section if nothing meets the bar.

### Files to Modify
Master table of every file that will be created or modified.

### Dependencies *(optional)*
Related issues, prerequisites, or things this supersedes.

---

## Quality Checks

Before presenting the draft, resolve every reference against the current codebase: file paths, line numbers, function signatures, invariant IDs. Mark a file as new where it does not exist yet. Run this silently and fix what fails — do not report the check.
