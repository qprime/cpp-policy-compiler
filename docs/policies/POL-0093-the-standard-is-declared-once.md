---
id: POL-0093
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tooling Commitments: standard"
  - source: cpp-convention/mechanisms.md
    locator: "A project declares its standard once"
---

# The language standard is declared once, in the build configuration

One declaration, in the top-level build configuration, and every target inherits
it. Reaching for a feature from a later standard than the one declared is a
defect, not an upgrade.

The reverse is also a defect. Using an older mechanism on a project that
declared a newer standard — a stream where `std::format` exists, an iterator
pair where `std::span` exists, `enable_if` where concepts exist — is the same
mistake in the other direction.

Every per-standard column in this corpus reads against this declaration. The
policy that says which spelling to use has no answer without it.

The declaration is what makes the mechanism guidance decidable at all: a rule of
the form "use the optional for your standard" needs a standard, and a project
that never stated one has to infer it from what currently compiles. A single
declaration also keeps the answer uniform across targets, which matters because
a feature that compiles in one target and not another produces a build failure
attributed to the target rather than to the version drift that caused it.
