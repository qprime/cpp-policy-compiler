# cpp-policy-compiler

A body of attributed C++ engineering policy, compiled into guidance documents
for LLM-driven projects.

## Why

When an LLM generates C++, its training is fixed; the only lever you hold at
generation time is what is in its context. Whatever judgment is not in context can
only be tested in afterward, through review and repair. This project takes the opposite approach: hold a curated corpus of
engineering judgment, and compile it into project-specific guidance that sits
in front of the model before it writes a line.

## How it's organized

Three authored layers and one derived:

- **Source** ([docs/source/](docs/source/)) — the material policies derive
  from: captured external documents and original testimony. Nothing here is
  guidance; it is the evidence guidance cites.
- **Policies** ([docs/policies/](docs/policies/)) — the opinionated layer, in
  five kinds: principles, standards, guidelines, patterns, and anti-patterns.
  Every policy is attributed to source and marked with where it applies.
- **Configurations** ([docs/configurations/](docs/configurations/)) —
  per-project facts on three axes: language version, compiler, domain.
- **Projections** — the compiled output: the policy body as seen through one
  configuration, rendered as a small always-loaded entry document plus topical
  documents under hard size budgets. Never authored, never edited, always
  regenerable.

A project consumes its projection by reference from its own harness files.
This tool never generates CLAUDE.md, AGENTS.md, or any other top-level
harness file.

## Design commitments

- The compile step is pure code. No LLM runs at compile time; the LLM assists
  at authoring time only.
- The tool is written in Python. The guidance it produces targets C++.
- Every piece of generated guidance is traceable to a stable decision identity
  and its source material.

## Status

Early design. Source material is captured; the first policies have not yet
been derived, and the compiler has not been written. The ontology above is
settled; most structure beneath it is not.

## License

[Apache-2.0](LICENSE)
