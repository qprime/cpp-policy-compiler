# Policies

The opinionated layer — the accumulated engineering judgment this project
exists to hold. Five kinds, defined in [CLAUDE.md](../../CLAUDE.md):
principles, standards, guidelines, patterns, anti-patterns.

Every policy carries three parts:

- **Content** — the guidance itself, written to render directly
- **Attribution** — the source it derives from; nothing enters unattributed
- **Applicability** — marks constrain out; absence means universal

Content is not only prose. A policy with a mechanical expression carries it
as an **enforcement facet** — clang-tidy checks, warning flags, format keys —
authored alongside the prose, never synthesized at compile time
([#1](https://github.com/qprime/cpp-policy-compiler/issues/1)). A pattern's
content may additionally take whole-file form: a compilable **skeleton**
exemplar, verified at projection build time
([#2](https://github.com/qprime/cpp-policy-compiler/issues/2)). Both are
renderings of the same decision identity as the prose.

The format below was derived from the first thirteen policies rather than
designed ahead of them. Every key exists because some policy could not be
expressed without it, and nothing appears that no policy needed. Deriving the
rest of the captured corpus took the count to ninety-three and added no key,
which is the evidence the format was read off real policies rather than
guessed. The projection topic list was then derived from the full corpus and
lives in [TOPICS.md](TOPICS.md).

## On-disk format

One file per policy, flat in this directory, named `POL-NNNN-<slug>.md`. One
decision per file, so each policy has its own history and its own citable
identity. Flat because the topic list must emerge from real policies — a
directory tree imposed now would invent the taxonomy the corpus is supposed to
reveal. Grouping earns itself later, or never.

### Identity

`POL-NNNN`, zero-padded, allocated highest-existing-plus-one. Never reused,
never reassigned. The identity encodes neither kind nor topic, because both can
change and identity cannot: a guideline promoted to a standard would otherwise
carry a lying id or need reassignment, and reassignment breaks every citation
already written. The slug in the filename is a human convenience; frontmatter
`id` is the citable thing, so renaming a slug breaks nothing.

### Frontmatter

| Key | Presence | Meaning |
|-----|----------|---------|
| `id` | required | `POL-NNNN`. Matches the filename prefix, unique across the corpus. |
| `kind` | required | One of `principle`, `standard`, `guideline`, `pattern`, `anti-pattern`. |
| `precedence` | principles only | Integer position in the total order; earlier beats later. Contiguous from 1. Appears on no other kind. |
| `applicability` | optional | Axis marks that constrain the policy out. Absent entirely means universal. |
| `attribution` | required | A list, never empty. Each entry carries `source` (path under `docs/source/`) and `locator` (where in that source), plus optional `upstream` (external citations by identity, e.g. Core Guidelines rule ids). One entry per distinct location, never merged. An entry with no `upstream` means the rule originates in this corpus. |
| `replacement` | anti-patterns only | List of ids where the replacement guidance lives. Every entry resolves to an existing policy. |
| `enforcement` | optional | Mechanical expressions of the policy, keyed by tool. Present only where one exists. Keys in use: `clang_tidy`, `warnings`, `sanitizers`, `clang_format`. A key's value takes whatever shape that tool's configuration takes — a list of checks or flags, a mapping of settings. |

Body is markdown, in three parts and in that order: the H1 carries the
statement, the next block carries the decision procedure a reader applies, and
the rationale comes last. Position ranks importance for a reader working under a
size budget, so a body that builds to its point inverts its own priority. There
is no `title` key, because the H1 is the title and duplicating it invites drift.

```yaml
---
id: POL-0010
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #7"
    upstream: ["CG ES.45"]
  - source: cpp-convention/conventions.md
    locator: "Trap: magic number"
enforcement:
  clang_tidy: ["readability-magic-numbers"]
---
```

An anti-pattern is authored in the same batch as the policy that replaces it,
never before. A `replacement` entry pointing at an id nobody has authored is a
dangling citation, so an anti-pattern whose replacement does not exist waits.

### Structural invariants

Asserted by the format, enforced by the compiler. Nothing in this directory
checks them.

- `id` is unique across the corpus and matches the filename prefix
- `kind` is one of the five
- `attribution` is present and non-empty on every policy
- `precedence` forms a contiguous total order across all principles and appears on no other kind
- `replacement` appears only on anti-patterns, and every entry resolves to an existing id

### Not in the format yet

- `skeleton`, a pattern's whole-file exemplar form. Eleven pattern policies now
  exist and none of them forced the field: each is expressible as prose plus a
  fragment, and a compilable whole-file exemplar is a build artifact with a
  verification step behind it. That is
  [#2](https://github.com/qprime/cpp-policy-compiler/issues/2) phase 2, and the
  field's shape follows from what the verification needs.
- `applicability` marks on the language-version and compiler axes. Version
  differences are content the projection selects among, not gates, so no policy
  yet needs one. When one does, it is the same key with a different axis name.

  The coroutine policies (POL-0080 through POL-0083) are the first case that
  presses on this. Their subject does not exist below C++20, so they are not
  wrong on a C++11 project, they are vacuous — and a vacuous entry still spends
  a projection's size budget. Whether *nothing to apply to* is a gate or content
  is undecided, and deciding it changes the format rather than any policy.

**Next:** /spec the v1 compiler. The topic list it renders is settled in
[TOPICS.md](TOPICS.md).
