# cpp-policy-compiler

One codebase, one reasoning mind. Developers express intent; the model
generates source. The project reads as though one experienced engineer made its
decisions: consistent standards, conventions, and judgment at every boundary.

This is a curated body of attributed C++ engineering policy, compiled into the
guidance documents an LLM reads before it writes code. It is for anyone running
an LLM-assisted C++ project who wants the model's output to be opinionated in a
specific, recorded way rather than in whatever way its training happened to
leave it.

## Why

When an LLM generates C++, its training is fixed; the only lever you hold at
generation time is what is in its context. Whatever judgment is not in context
can only be tested-in afterward, through review and repair. This project takes
the opposite approach: hold a curated corpus of engineering judgment, and
compile it into project-specific guidance that sits in front of the model
before it writes a line.

The target is reasoning consistency, not style consistency. Each policy
resolves a decision — in this situation, we do this, because — so the model
inherits the decision rather than making its own. When generated code needs
correcting, the durable fix is an amendment to the corpus, not just to the
file.

## Quickstart

Python 3.12 or newer. The repository is a [uv](https://docs.astral.sh/uv/)
project, so no separate install step is needed:

```
uv run polc build \
  --config docs/configurations/cpp20-gcc-application.md \
  --out ../my-project/policy
```

That reads the whole corpus, selects the subset the configuration admits, and
writes a projection — about two dozen markdown documents plus the exemplar
source trees. `polc check` takes the same arguments minus `--out`, validates
and renders, and writes nothing; use it to see what a configuration would emit,
or in CI to catch a corpus that no longer compiles.

Point your project's own instructions at `index.md` and the model routes itself
from there. For Claude Code, skip that step:

```
uv run polc build \
  --config docs/configurations/cpp23-gcc-realtime.md \
  --out ../my-project/.claude/skills/cpp-policy \
  --adapter claude-code
```

`--adapter claude-code` names the entry document `SKILL.md` and gives it skill
frontmatter, so the output directory is a working skill as written. Nothing
polc emits executes in the target project — the output is text and a map.

Both invocations own their output directory. Regeneration overwrites hand
edits, and every rendered document says so in a banner on its first line.

## What a projection contains

One entry document plus the documents it routes to.

`index.md` (or `SKILL.md`) is the always-loaded part: the configuration's three
axes, the principles, a legend defining the `MUST` / `SHOULD` / `THIS WAY` /
`NEVER` marks that head every rule, and a map. The map is the routing
mechanism — one line per document, each saying when to read it. The model
reads the entry document, matches the situation in front of it to a line, and
opens that one document.

The map covers the coding standard, one document per topic, the exemplars, and
project setup. Alongside them sits `exemplars/`, the copied source trees, and
`provenance.json`, a machine-readable index from every emitted id back to its
attribution and source file.

## How it's organized

Five authored layers and one derived:

- **Source** ([docs/source/](docs/source/)) — the material policies derive
  from: captured external documents and original testimony. Nothing here is
  guidance; it is the evidence guidance cites.
- **Policies** ([docs/policies/](docs/policies/)) — the opinionated layer, in
  five kinds: principles, standards, guidelines, patterns, and anti-patterns.
  Every policy is attributed to source and marked with where it applies.
  [TOPICS.md](docs/policies/TOPICS.md) partitions them into twenty topics by
  the task a reader is in the middle of — choosing a representation, handling
  failure, crossing the FFI boundary — and each topic becomes one document in
  the projection. Every non-principle policy belongs to exactly one topic, so a
  reader is never deciding between two homes for the same rule.
- **Standard** ([docs/standard/](docs/standard/)) — the decided-once layer:
  file layout, naming, line layout, comments, and toolchain. Each entry fixes
  one value that every file follows and that a tool or a glance can check.
- **Exemplars** ([docs/exemplars/](docs/exemplars/)) — whole compilable source
  trees, each showing a recurring situation as header, implementation, and
  adjacent tests. An exemplar cites the policy and standard ids it
  demonstrates rather than restating them.
- **Configurations** ([docs/configurations/](docs/configurations/)) —
  per-project facts on three axes: language version, compiler, domain. A
  configuration is what selects the subset; a C++23 realtime project and a
  C++20 application project get different documents from the same corpus.
- **Projections** — the compiled output, described above. Regenerable from the
  corpus, and not meant to be edited.

## Design commitments

- The compile step is pure code. No LLM runs at compile time; the LLM assists
  at authoring time only.
- The tool is written in Python. The guidance it produces targets C++.
- Every piece of generated guidance is traceable to a stable decision identity
  and its source material.
- The projection ships no retrieval logic. The model is the retriever; what
  ships is text and a map.

## Status

Early, and under active design. The corpus holds 249 policies, 29 standard
entries, and 14 exemplars, and two configurations are authored. The compiler
validates and renders both end to end.

The compile path has no test harness yet — changes are verified by building
both configurations and reading the output. Treat the projection format as
unstable until it does.

## License

[Apache-2.0](LICENSE)
