# CLAUDE.md — cpp-policy-compiler

A curated body of attributed C++ engineering policy, compiled by a pure-Python
tool into the guidance documents an LLM reads before it writes code. The
architecture is under active design.

The compiler is Python. Everything it compiles targets C++.

## Expertise

| Area | Why this project needs it |
|---|---|
| C++ engineering practice | The corpus is C++ judgment. Every policy, standard entry, and exemplar has to be right about C++. |
| Python tooling | `polc` is the compiler: a deterministic corpus → projection pipeline. |
| Structured-knowledge authoring | Policies carry attribution, stable ids, and applicability marks. Identity and provenance are the product. |
| LLM context design | A projection is read by a model, not a person. Routing tables, trigger keys, and document boundaries are the design surface. |

## Look-Up Map

| Document | Location | Role | When to use it |
|---|---|---|---|
| Project overview | [README.md](README.md) | What polc is, what a projection contains, how the corpus is organized | Orientation, and before changing the projection format |
| Source | [docs/source/](docs/source/) | Captured external documents and original testimony | Tracing what a policy cites |
| Policies | [docs/policies/](docs/policies/) | The opinionated layer: principles, standards, guidelines, patterns, anti-patterns | Authoring or amending an opinion |
| Topic partition | [docs/policies/TOPICS.md](docs/policies/TOPICS.md) | Assigns every non-principle policy to exactly one of twenty topics | Deciding where a new policy lives |
| Standard | [docs/standard/](docs/standard/) | The decided-once layer: layout, naming, comments, toolchain | Fixing a single value every file follows |
| Exemplars | [docs/exemplars/](docs/exemplars/) | Whole compilable source trees demonstrating a recurring situation | Adding or changing a worked example |
| Configurations | [docs/configurations/](docs/configurations/) | Per-project axes — language version, compiler, domain — that select the corpus subset | Changing what a projection admits |
| Python conventions | [docs/conventions/python.md](docs/conventions/python.md) | Patterns and traps for the compiler source | Writing anything under `src/` |
| Markdown conventions | [docs/conventions/markdown.md](docs/conventions/markdown.md) | Formatting for root documents and specs. Corpus documents follow their own layer's on-disk format instead. | Authoring a root document or a spec |
| Review log | [REVIEW-NOTES.md](REVIEW-NOTES.md) | Durable findings not yet ready to become corpus or code changes | Recording a review result with no immediate change |
| Specs | GitHub issues on `qprime/cpp-policy-compiler` | Implementation specs and the work loop | Every change large enough to spec |

## Capabilities

| Behavior | What it means |
|---|---|
| Artifact-On-Request | When the user asks for an artifact, produce the artifact. Where the architecture says it should be generated rather than authored, say so in one sentence and produce it anyway. A design decision in this repository never outranks a direct request. |
| Ask-Don't-Reframe | Never restate the user's request as a different request. Where you believe they want something other than what they said, ask in one sentence, then do what they said. |
| Identity-Is-Permanent | Policy, standard, and exemplar ids are cited from projections and from provenance records. Never renumber, reuse, or silently retire one. |
| Compile-Stays-Pure | No LLM runs at compile time. Keep `polc` deterministic: same corpus and configuration in, same projection out. |
| Verify-By-Building | The compile path has no test harness. Verify a change by building both configurations in `docs/configurations/` and reading the output. |

## Skill Routing

| User says | Use |
|---|---|
| "is this the right approach", a tradeoff, a design question about existing code | `/architect` |
| "write it up", "spec this", ready to open an issue | `/spec` |
| "implement", "fix", "build it" | `/engineer` |
| "review this", a PR, an issue, the working diff | `/review` |
| "clean this doc up", residue in a settled document | `/clean-slop` |
| Create or update `CLAUDE.md`, `README.md`, `GLOSSARY.md`, `ONTOLOGY.md`, `INVARIANTS.md` | `/generate` |
| Pull a YouTube transcript | `/fetch-yt-transcripts` |
