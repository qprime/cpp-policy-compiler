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
edits, and every rendered document says so in a banner on its first line. The
copied configuration carries no banner, since it is a verbatim copy rather than
a rendered document. `layers.md` and `invariants.md` carry no banner either:
polc seeds them once with a note saying what the project writes there, and
after that leaves whatever it finds in place.

## What a projection contains

One entry document plus the documents it routes to.

`index.md` (or `SKILL.md`) is a pointer file: the configuration's three axes,
the polc version and corpus fingerprint the projection was built from, a
four-step procedure, and a map. The procedure fixes the order of operations —
take the shape from the nearest exemplar, check each construct you write
against a trigger table, read the layer semantics, read the subsystem
invariants. The map is the routing mechanism the second step uses: one line per
document, each saying when to read it. The model reads the entry document,
matches the situation in front of it to a line, and opens that one document.

Each lookup the procedure names is a table rather than a judgment call.
`exemplars.md` opens with one row per exemplar keyed by the situation it
answers, and each topic document opens with one row per rule keyed by the
construct you are about to write. `principles.md` is where the second step
lands when no trigger row matches: the principles, which apply to every
decision rather than to a situation, and a legend defining the `MUST` /
`SHOULD` / `THIS WAY` / `NEVER` marks that head every rule. The map does not
route to it.

Steps three and four land in `layers.md` and `invariants.md`, the two documents
the project writes itself. polc seeds each once and never overwrites it, because
what the layers are and what each subsystem guarantees are facts about the
target project rather than about the corpus.

The map covers the coding standard, one document per topic, the exemplars, and
project setup. Alongside them sits `exemplars/`, the copied source trees;
`configuration.md`, a verbatim copy of the configuration the projection was
built from; and `provenance.json`, which holds a `projection` block naming the
polc version, a SHA-256 fingerprint of the corpus, the configuration, and the
adapter, and an `entries` block indexing every emitted id back to its
attribution and source file.

The fingerprint covers every file under the policies, standard, and exemplars
directories, so a projection in a target repository can be compared against a
fresh build by reading one line.

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

[docs/conventions/](docs/conventions/) is not one of these layers. It holds house
rules for writing the compiler and this repository's own documents. `polc` never
reads it, and nothing in it reaches a projection.

## Design commitments

- The compile step is pure code. No LLM runs at compile time; the LLM assists
  at authoring time only.
- The tool is written in Python. The guidance it produces targets C++.
- Every piece of generated guidance is traceable to a stable decision identity
  and its source material.
- The projection ships no retrieval logic. The model is the retriever; what
  ships is text and a map.

## Status

Early, and under active design. The corpus holds 247 policies, 29 standard
entries, and 14 exemplars, and two configurations are authored. The compiler
validates and renders both end to end.

The compile path has no test harness yet — changes are verified by building
both configurations and reading the output. Treat the projection format as
unstable until it does.

## License

[Apache-2.0](LICENSE)
