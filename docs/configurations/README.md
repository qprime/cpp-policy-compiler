# Configurations

Per-project constraints — facts, not opinions. Three axes, each a
whole-project fact:

- **Language version** — C++14 / 17 / 20 / 23
- **Compiler** — gcc and clang to start
- **Domain** — e.g. embedded, realtime, application

A configuration selects the policy subset for one project; the compiler
projects the body of policy through it. Axes gain granularity only when a
real policy demands gating.

**Next:** write the first configuration when the first projection is
attempted.
