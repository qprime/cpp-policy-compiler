# cpp-policy-compiler
One codebase, one reasoning mind. Developers express intent; the model generates source. The project reads as though one experienced engineer made its decisions: consistent standards, conventions, and judgment at every boundary.

This project contains a body of attributed C++ engineering policy, compiled into guidance documents
for LLM-driven projects. These documents are intended to be imported into new and existing LLM-assisted software projects.

## Why

When an LLM generates C++, its training is fixed; the only lever you hold at
generation time is what is in its context. Whatever judgment is not in context
can only be tested-in afterward, through review and repair. This project takes
the opposite approach: hold a curated corpus of engineering judgment, and
compile it into project-specific guidance that sits in front of the model
before it writes a line.

The target is reasoning consistency, not style consistency: the whole
codebase should read as the work of one opinionated senior engineer. Each
policy resolves a decision — in this situation, we do this, because — so the
model inherits the decision rather than making its own. Engineers express
intent through this surface, and when generated code needs correcting, the
durable fix is an amendment to the surface, not just to the file.

## How it's organized

Five authored layers and one derived:

- **Source** ([docs/source/](docs/source/)) — the material policies derive
  from: captured external documents and original testimony. Nothing here is
  guidance; it is the evidence guidance cites.
- **Policies** ([docs/policies/](docs/policies/)) — the opinionated layer, in
  five kinds: principles, standards, guidelines, patterns, and anti-patterns.
  Every policy is attributed to source and marked with where it applies.
- **Standard** ([docs/standard/](docs/standard/)) — the decided-once layer:
  file layout, naming, line layout, comments, and toolchain. Each entry fixes
  one value that every file follows and that a tool or a glance can check.
- **Exemplars** ([docs/exemplars/](docs/exemplars/)) — whole compilable source
  trees, each showing a recurring situation as header, implementation, and
  adjacent tests. An exemplar cites the policy and standard ids it
  demonstrates rather than restating them.
- **Configurations** ([docs/configurations/](docs/configurations/)) —
  per-project facts on three axes: language version, compiler, domain.
- **Projections** — the compiled output: the corpus as seen through one
  configuration. An entry document carries the principles, a legend for the
  `MUST` / `SHOULD` / `THIS WAY` / `NEVER` marks, and a map routing to every
  other document — the coding standard, one document per topic, the exemplars
  with their source trees, and project setup. Every rendered document declares
  itself generated; regeneration overwrites hand edits.

A target project takes a projection by pointing its own instructions at the
entry document. `polc build --adapter claude-code` names that document
`SKILL.md` and prepends skill frontmatter instead, so the output directory
drops into `.claude/skills/` as-is. Nothing polc emits executes in the target
project.


## Design commitments

- The compile step is pure code. No LLM runs at compile time; the LLM assists
  at authoring time only.
- The tool is written in Python. The guidance it produces targets C++.
- Every piece of generated guidance is traceable to a stable decision identity
  and its source material.

## License

[Apache-2.0](LICENSE)
