# cpp-policy-compiler

`cpp-policy-compiler` gives a C++ project a maintained set of engineering
decisions for coding agents. It combines a canonical C++ policy corpus with the
facts and exceptions of one project, then generates two documentation harnesses:

- **generation** guidance for writing code;
- **review** guidance for inspecting an existing change.

The result is ordinary Markdown and example source. Nothing generated executes
inside the target project, and compiling a harness never calls an LLM.

## Why

Coding models know C++, but they do not automatically know a project's choices
about ownership, errors, interfaces, concurrency, testing, or architecture.
When those decisions are absent, the model guesses and reviewers rediscover the
same disagreements repeatedly.

This project records those decisions once and puts the applicable subset in the
agent's context. Every generated rule has a stable identity and provenance, so
a weak result can lead to a durable policy improvement rather than only a
one-file repair.

## Use it in a project

Python 3.12 or newer is required. Once a release is published, install and pin
the tool:

```text
pipx install polc==0.1.0
```

Initialize a target project:

```text
polc project init \
  --root ../my-project \
  --language-version 20 \
  --compiler gcc \
  --domain application
```

This creates project-owned inputs under `.polc/` and generated guidance under
`policy/generation/` and `policy/review/`. Describe the project's architecture
in `.polc/context/layers.md` and its load-bearing guarantees in
`.polc/context/invariants.md`, then rebuild:

```text
polc project build --root ../my-project
```

Point the coding agent at `policy/generation/index.md` when it writes code and
the reviewing agent at `policy/review/index.md` when it reviews code. Check the
generated directories and `.polc/` inputs into the target repository.

Use the read-only drift check in CI:

```text
polc project check --root ../my-project
```

Local policies, exclusions, replacements, standards, and exemplars live under
`.polc/`. They belong to the target project and evolve with it. See
[Adopting and maintaining a harness](docs/adopting.md) for overlays, Claude Code
integration, upgrades, and the lower-level compiler commands.

## What gets generated

Each harness has one entry document and a set of focused documents to which it
routes the agent. The selected policy identities are the same in both modes,
but their routes differ:

- Generation routes from the construct about to be written and includes
  complete exemplar source trees.
- Review routes from observable evidence in a change and omits exemplar
  implementations so that the review remains independent.

Both include the target project's layers and invariants. `provenance.json`
records the compiler version, corpus fingerprint, configuration, mode, and the
source of every emitted identity.

## What lives in this repository

- [Policies](docs/policies/) hold attributed engineering decisions, organized
  into twenty task-oriented topics.
- [The standard](docs/standard/) holds decided-once, mechanically visible
  choices such as naming, layout, warnings, and build tools.
- [Exemplars](docs/exemplars/) are complete source trees showing recurring
  situations.
- [Configurations](docs/configurations/) select policies by C++ version,
  compiler, and domain.
- [Source material](docs/source/) is evidence from which policies derive; it is
  not itself generated guidance.

The compiler validates, selects, renders, and packages these layers. It does not
format or rewrite a target project's C++ source.

## Development

This repository is a [uv](https://docs.astral.sh/uv/) project:

```text
uv run polc check \
  --config docs/configurations/cpp20-gcc-application.md
uv run pytest -q
```

Repository authors can build a projection directly with `polc build`. Consumers
should normally use the managed `polc project` workflow above. Text-only release
archives provide a no-tool alternative; see [Distribution](docs/distribution.md).

Correctness evaluation is explicit and opt-in. It measures how a recorded
harness performs on a particular task and is never part of normal project
builds. See [Correctness benchmarks](benchmarks/README.md).

## Status

The end-to-end harness, project overlay lifecycle, paired projections,
distribution paths, and correctness evaluator are implemented and tested. The
corpus currently contains 247 policies, 29 standard entries, 14 exemplars, and
two stock configurations.

The current maturity frontier is policy content. Structural validation cannot
prove that every C++ decision is technically correct or properly scoped. The
[canonical corpus audit](https://github.com/qprime/cpp-policy-compiler/issues/28)
tracks that review before broad brownfield normalization.

Maintainers record that semantic review under [`audits/corpus-v1/`](audits/corpus-v1/).
`polc audit check --root audits/corpus-v1` deterministically checks inventory and
report coverage; it does not attempt to score technical correctness.

The original [project harness design](https://github.com/qprime/cpp-policy-compiler/issues/17)
records the reasoning behind the managed lifecycle and distribution model.

## License

[Apache-2.0](LICENSE)
