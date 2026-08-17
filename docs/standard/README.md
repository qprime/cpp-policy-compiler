# Coding standard

The decided-once layer. Every entry here fixes a value that every file follows and
that a tool or a glance can check. What follows is the on-disk format.

The split against [the policy corpus](../policies/) is
[STANDARD-TOPICS.md](../policies/STANDARD-TOPICS.md): a standard entry is a value
the project decided once; a policy is a decision procedure an author applies case
by case. The rule that keeps a policy from restating what lands here is in
[the corpus format](../policies/README.md#the-coding-standard-boundary).

## On-disk format

One file per entry, flat in this directory, named `STD-NNNN-<slug>.md`. Flat for
the same reason the corpus is flat: the grouping is frontmatter, so a regrouping is
an edit to one key rather than a directory move that breaks every citation.

### Identity

`STD-NNNN`, zero-padded, allocated highest-existing-plus-one. Never reused, never
reassigned. The identity encodes neither group nor output, because both can change
and identity cannot. The slug in the filename is a human convenience; frontmatter
`id` is the citable thing.

### Frontmatter

| Key | Presence | Meaning |
|-----|----------|---------|
| `id` | required | `STD-NNNN`. Matches the filename prefix, unique across the standard. |
| `group` | required | One of `files-and-layout`, `names`, `layout-of-the-line`, `comments`, `toolchain`. Decides the entry's section, and which document it renders into. |
| `enforced_by` | required | Who catches a violation: `compiler`, `clang-format`, `clang-tidy`, `build`, or `review`. `review` means nothing automatic checks it. |
| `applicability` | optional | Axis marks that constrain the entry out, same axes as a policy. Absent entirely means universal, which is the usual case. |
| `attribution` | required | A list, never empty, same shape as a policy's: `source` and `locator`, plus optional `upstream` for Core Guidelines rule ids. |

```yaml
---
id: STD-0004
group: files-and-layout
enforced_by: clang-tidy
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: module boundary"
    upstream: ["CG SF.8"]
---
```

### Body

The H1 carries the statement. What follows is the value — a table, a list, or a
code block — and then nothing.

**Rationale is omitted by default.** This is the one real difference from a policy
body. A policy ends in rationale because its reader has to apply judgment; a
standard entry ends when the value is stated. Most of these choices have no reason
beyond *we picked one*, and inventing one invites the next reader to relitigate it.

Write a closing line **only where its absence invites reversal** — where a reader
who does not know the reason would helpfully change the value back. `#pragma once`
in [STD-0004](STD-0004-include-guards.md) and `.h` in
[STD-0001](STD-0001-file-extensions.md) are the shape of that case. Where the
reason is *we picked one*, say nothing.

### Outputs

`group` decides which document an entry renders into.

| Document | Groups | Read by |
|----------|--------|---------|
| `standard.md` | files-and-layout, names, layout-of-the-line, comments | Anyone, or anything, writing a file |
| `project-setup.md` | toolchain | Whoever starts or reconfigures a project |

The standard is rendered whole into its document — every entry, every time — which
is why there is no manifest and no `Read when` line. The policy corpus is projected
selectively and needs both.

### What a standard entry does not have

- **No `precedence`.** Entries state disjoint values; nothing conflicts, so there
  is no order to resolve.
- **No `replacement`, and no anti-patterns.** An entry states the value, which
  makes every other value wrong without a second document saying so.
- **No topic membership.** `group` is the whole grouping, and the standard is
  always loaded in full.

### Structural invariants

Asserted by the format. No compiler enforces them yet — the loader and the two
render targets are unbuilt.

- `id` is unique across the standard and matches the filename prefix
- `group` is one of the five
- `enforced_by` is one of the five
- `attribution` is present and non-empty on every entry
- every topic in [STANDARD-TOPICS.md](../policies/STANDARD-TOPICS.md) resolves to
  exactly one entry, and every entry resolves to exactly one topic

### Open format question

**Whether a policy may cite an entry by id.** A policy that relies on a standard
fact currently names the mechanism in prose, which nothing validates — a policy can
name a warning set the standard stopped having. An `enforces` or `relies_on` key
holding `STD-NNNN` would make the reference checkable the way `replacement` already
is. It waits on the loader, since there is nothing to resolve against yet.
