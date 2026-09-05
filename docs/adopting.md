# Adopting and maintaining a harness

The managed project workflow is the normal way to use `polc`. It keeps the
canonical corpus versioned with the compiler while giving the target repository
ownership of its local decisions and context.

## Initialize

```text
polc project init \
  --root ../my-project \
  --language-version 20 \
  --compiler gcc \
  --domain application
```

Initialization creates:

```text
.polc/
  project.md
  lock.json
  context/
    layers.md
    invariants.md
  policies/
  standard/
  exemplars/
policy/
  generation/
  review/
```

`project.md` records selection facts and local exclusions or replacements.
The other authored directories extend the canonical corpus. The lock pins the
compiler, corpus fingerprint, projection format, adapter, and managed output
locations.

Generated output directories are owned by `polc`; regeneration replaces them.
Make project-specific edits under `.polc/`, not inside a projection.

## Maintain project context

Write architectural dependency and failure boundaries in
`.polc/context/layers.md`. Write subsystem guarantees that must remain true in
`.polc/context/invariants.md`. Both documents are copied into generation and
review projections.

After changing context or a local policy input, rebuild both projections:

```text
polc project build --root ../my-project
```

Check for missing rebuilds in CI without writing files:

```text
polc project check --root ../my-project
```

## Change the canonical release

Installing a different `polc` package does not silently change a target
project's guidance. Preview the executing package and corpus:

```text
polc project diff --root ../my-project
```

The preview reports version and fingerprint changes, affected policy identities,
and changed generated files. Accept the candidate only after reviewing it:

```text
polc project accept --root ../my-project
```

Acceptance updates the lock and both projections together. Incompatible lock or
projection formats fail with the locked and executing versions named.

## Local decisions

A target project can:

- exclude a canonical topic or identity with a recorded reason;
- replace a canonical policy or standard entry with a local identity;
- add project-specific policies and topic membership;
- add complete local exemplars.

Stable identities make these changes visible in provenance and upgrade diffs.
Replacing a policy does not automatically transfer an exemplar's evidence. A
retained exemplar must still truthfully demonstrate every identity it cites;
otherwise exclude it or provide compatible local source.

## Claude Code layout

Initialize with an adapter when the target uses Claude Code:

```text
polc project init \
  --root ../my-project \
  --language-version 20 \
  --compiler gcc \
  --domain application \
  --adapter claude-code
```

This emits independent generation and review skills under `.claude/skills/`,
with `SKILL.md` entry points and appropriate frontmatter. Switch an existing
managed harness with:

```text
polc project accept --root ../my-project --adapter claude-code
polc project accept --root ../my-project --adapter neutral
```

Only output directories whose provenance proves `polc` ownership are replaced
or removed.

## Lower-level repository commands

Corpus authors can validate or build one projection without creating a managed
target:

```text
polc check --config docs/configurations/cpp20-gcc-application.md
polc build \
  --config docs/configurations/cpp20-gcc-application.md \
  --mode review \
  --out /tmp/policy-review
```

Generation is the default mode. `--mode review` selects the independent review
routes. `--adapter claude-code` changes an individual build's entry document to
`SKILL.md`.

The `--policies`, `--standard`, and `--exemplars` overrides exist for repository
development and candidate-corpus testing. Installed managed projects normally
use the matching corpus bundled in the pinned wheel.
