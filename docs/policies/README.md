# Policies

The opinionated layer — the accumulated engineering judgment this project exists
to hold. The corpus is empty pending a rebuild; what follows is the on-disk
format the compiler enforces.

Every policy carries three parts:

- **Content** — the guidance itself, written to render directly
- **Attribution** — the source it derives from; nothing enters unattributed
- **Applicability** — marks constrain out; absence means universal

Content carries the code that shows the guidance, not prose alone. A rule stated
without an example is a rule the reader has to imagine, and the reader here is a
pattern-matcher.

## On-disk format

One file per policy, flat in this directory, named `POL-NNNN-<slug>.md`. One
decision per file, so each policy has its own history and its own citable
identity. Flat because the topic list must emerge from real policies; a
directory tree imposed up front invents the taxonomy the corpus is supposed to
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
| `applicability` | optional | Axis marks that constrain the policy out. Axes are `language_version`, `compiler`, `domain`. Absent entirely means universal. |
| `attribution` | required | A list, never empty. Each entry carries `source` and `locator`, plus optional `upstream` for external citations by identity, such as Core Guidelines rule ids. `source` is a path under `docs/source/` with `locator` naming the place in it, or the literal `standard-practice` for a rule that is settled C++ practice rather than a position this corpus took, with `locator` naming the area. One entry per distinct location, never merged. An entry with no `upstream` means the rule originates in this corpus. |
| `replacement` | anti-patterns only | List of ids where the replacement guidance lives. Every entry resolves to an existing policy. |

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
---
```

Body is markdown, in three parts and in that order: the H1 carries the
statement, the next block carries the decision procedure a reader applies, and
the rationale comes last. Position ranks importance for a reader who may stop
early, so a body that builds to its point inverts its own priority. There is no
`title` key, because the H1 is the title and duplicating it invites drift.

An anti-pattern is authored in the same batch as the policy that replaces it,
never before. A `replacement` entry pointing at an id nobody has authored is a
dangling citation, so an anti-pattern whose replacement does not exist waits.

### Structural invariants

Asserted by the format, enforced by the compiler. Nothing in this directory
checks them.

- `id` is unique across the corpus and matches the filename prefix
- `kind` is one of the five
- `attribution` is present and non-empty on every policy
- `precedence` forms a contiguous total order across all principles and appears
  on no other kind
- `replacement` appears only on anti-patterns, and every entry resolves to an
  existing id
- every non-principle policy is a member of exactly one topic in
  [TOPICS.md](TOPICS.md)
- every anti-pattern shares a topic with at least one non-principle replacement

### Open format questions

Neither is decided, and deciding either changes the format rather than any
policy.

- **A pattern's whole-file exemplar.** Pattern policies carry a fragment, which
  shows the shape of a construct but not the shape of a file: header discipline,
  namespace, ordering. A `skeleton` field waits on authoring the first exemplar,
  because the field's shape follows from what a whole file turns out to need.
- **Vacuous versus excluded.** A policy whose subject does not exist below a
  given standard is not wrong on an older project, it is vacuous, and a vacuous
  entry is one more thing a reader has to rule out. Whether *nothing to apply
  to* is an `applicability` gate or content the projection selects among is
  undecided. Coroutines is the clearest case.
