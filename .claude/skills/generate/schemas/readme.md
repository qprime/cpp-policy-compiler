# README.md

Artifact: `README.md` at the repository root. Unconditional — every project has one.

## Sections

Write the sections in this order. Omit an optional section when it does not apply.
Do not omit, reorder, or add anything else.

### Header

An H1, one bolded declarative tagline, then one to three sentences of framing that
elaborate on it rather than restate it. Name what the project does for the reader,
in their terms.

Where one hard constraint shapes everything — offline, CPU-only, sub-100ms, single
binary — give it its own short line.

### What This Is

What the project does for the reader: the families of things it handles, the shape
of a typical job, what comes out. Walk one canonical example end to end — input,
intermediate, output.

Answer what someone can do with the project. Leave how it is built to `CLAUDE.md`.

### How To Use

Numbered subsections with copy-pasteable commands tied to something real in the
repo. Mark what needs credentials or network, and mark what runs offline.

Shape the section to how someone engages the project:

| Project shape | Section becomes |
|---|---|
| Evaluation / research | install, get data, run, tests |
| Library / CLI | install, then a minimal call |
| Agent-driven | install, how to start a session, what to ask for first |
| Reading-shaped corpus | entry points, order, what skimming vs reading gets you |

### Scope Boundaries

A two-column `In scope | Out of scope` table, four to eight rows. Pair each
out-of-scope item with its in-scope counterpart on the same axis.

Name what the project deliberately is not. Do not write a roadmap.

### Requirements *(optional)*

Write this section when the project has an installable surface. Give the language
version, the key dependencies, and a link to the manifest.

### License

Use this text unless the project is genuinely open:

```
Copyright © [year] [Name]. All rights reserved.

This repository is published for portfolio and review purposes. No license is
granted to use, copy, modify, or distribute this code or its contents. If you're
interested in using any part of this work, please get in touch.
```

Where the project ships or references third-party data carrying its own terms, add
a paragraph stating those terms are independent of this repository's.
