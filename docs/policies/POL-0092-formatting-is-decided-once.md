---
id: POL-0092
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments: formatting"
---

# Formatting is decided once per project and applied by the tool

Every project has a `clang-format` configuration, committed, and every file
conforms to it. The baseline is `BasedOnStyle: Google` with `IndentWidth: 4` and
`ColumnLimit: 100`.

Details beyond the baseline are a per-project choice. That there is a
configuration, and that it is applied rather than approximated by hand, is not.

Formatting is not a matter of judgment once the file is committed, so it is the
one part of a convention that should never be discussed again. A tool applies it
in full, which is what makes that possible.

An unformatted or hand-formatted tree makes every diff carry changes nobody
made. Reformatting noise buries the change under review, and it makes the
history useless for the question of when a line last actually changed. The
baseline is stated rather than left open because a project with no configuration
does not stay unformatted, it acquires several formats, one per author, and
converging afterward costs a commit that touches every file.
