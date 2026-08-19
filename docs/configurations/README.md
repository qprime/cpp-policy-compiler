# Configurations

Per-project constraints — facts, not opinions. Three axes, each a
whole-project fact:

- **Language version** — C++14 / 17 / 20 / 23
- **Compiler** — gcc and clang to start
- **Domain** — e.g. embedded, realtime, application

A configuration selects the policy subset for one project; the compiler
projects the body of policy through it. Axes gain granularity only when a
real policy demands gating.

The first configuration is
[cpp20-gcc-application.md](cpp20-gcc-application.md); `polc build --config
docs/configurations/cpp20-gcc-application.md --out <dir>` projects through it,
emitting the entry document, the coding standard, project setup, one document
per topic, and the exemplar source trees. Add `--adapter claude-code` to name
the entry document `SKILL.md` and give it skill frontmatter.

**Next:** add a configuration when a real project needs one.
