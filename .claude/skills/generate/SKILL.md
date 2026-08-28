---
name: generate
description: Create or update one of the project's permanent root documents — CLAUDE.md, README.md, GLOSSARY.md, ONTOLOGY.md, INVARIANTS.md — against the schema that defines its shape.
argument-hint: <artifact.md>
disable-model-invocation: true
---

# /generate

Create or update: $ARGUMENTS

## Resolve the schema

Match the argument against the files in `schemas/`. `claude.md`, `CLAUDE.md`, and
`claude` all resolve to `schemas/claude.md`.

Read that one schema. Read no others.

Where nothing matches, list the files in `schemas/` and stop.

## Create or update

The schema fixes the shape. The repository supplies the content. Read the
repository before you write anything.

**The artifact does not exist.** Write it, following the schema's sections in its
order.

Before you write an earned artifact, check that the project has the material the
schema names. Where it does not, refuse, say what is missing, and write nothing.
Do not route the content into a different artifact instead — a glossary's
definitions written into `CLAUDE.md` because `GLOSSARY.md` is missing lands them
in the one file that costs tokens every turn.

**The artifact exists.** Edit only what the schema or the repository contradicts.
Leave correct prose byte-for-byte.

## Report

Say what you changed and why. Then report what you found and did not fix:

- A section out of order, missing, or not in the schema
- A path, invariant ID, or command name the artifact references that no longer
  resolves
- A row or section pointing at a document the project does not have

Point at a document only where that document exists. Where a schema's section
depends on an absent artifact, omit the section and name the command that would
produce it. Never fill a missing target by inlining what it would have held.

## Link it

After writing an artifact that did not exist, add one row to the Look-Up Map in
`CLAUDE.md` — the document, its location, its role, and when to use it.

Skip this when the artifact is `CLAUDE.md`, when `CLAUDE.md` does not exist, or
when it already names the artifact. Never create `CLAUDE.md` here, and never add
the Look-Up Map section where it is missing — report that instead.

One row is the whole blast radius. Nothing else in `CLAUDE.md` changes.

An artifact nobody links is invisible. The agent finds code by searching and
cannot discover a document without being told.
