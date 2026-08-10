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

No on-disk format yet — the first real policies force that decision, along
with the projection topic list. Whatever format emerges must carry these
content forms.

**Next:** derive the first policies from captured source.
