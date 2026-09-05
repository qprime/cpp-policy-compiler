# Distribution acceptance

Run on 2026-09-04 with the locally built `polc-0.1.0` wheel. All target operations
used the installed `polc` executable from outside this checkout and omitted corpus
path flags.

## Pinned targets

| Target | Revision | Project facts |
|---|---|---|
| empty directory | none | C++20, GCC, application |
| `qprime/mill_ui` | `29b4662587758c1359ae16d7869c4139af89480f` | C++20, Clang, application |
| `qprime/relay` | `83ad8ffac5c3075c19c43bddc348c17477e34c58` | C++23, GCC, realtime |

Both repositories were disposable clones. Existing `CLAUDE.md` hashes were recorded
before initialization and remained identical afterward. The real worktrees were not
modified.

## Procedure and result

The empty target initialized and checked successfully. Two builds produced identical
trees. Appending a line to `policy/generation/index.md` made `project check` exit 1 and
name that file; `project build` restored it, and the next check passed. The resulting
text remained ordinary readable Markdown after the temporary tool environment was no
longer involved.

For `mill_ui`, initialization preserved its existing instructions and `.claude`
commands. The maintained summaries under `contexts/mill-ui-*` were copied into
`.polc/context/`, then propagated byte-for-byte into both projections. Two generated
trees hashed identically at
`bb09df88628b6ca66e2bb22adf22fbc1da6d8e2bb4f9236f27b4e8199718bf4e`.

For Relay, the maintained summaries under `contexts/relay-can-*` capture the task-spec,
strategy, simulator, host, arbitration, clock, and verification boundaries relevant to
CAN. They propagated byte-for-byte into both projections. Two generated trees hashed
identically at
`f3299e5a978e661f3b7a33d74075963fe163bc83db0ed189f1b7c23e621582a5`.

Rich source documents were not copied verbatim. Their internal relative links are
based at their original documentation directories and correctly fail generated-link
validation after relocation. The self-contained summaries are the maintained overlay
contract for this format; automatic link rebasing or recursive context packaging is a
future feature, not silent behavior.

The Relay correctness experiment was not rerun. Its separately measured generation
and review evidence remains in [`../relay-can/RESULTS.md`](../relay-can/RESULTS.md): the
generation projection was faster but produced the weaker implementation, while the
independent review projection found additional adjudicated defects. This acceptance
only establishes that the same released corpus, paired modes, and Relay-specific
context compile and maintain deterministically.
