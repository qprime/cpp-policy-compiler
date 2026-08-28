# ONTOLOGY.md

Artifact: `ONTOLOGY.md` at the repository root. Earned when the domain has
relations a reader cannot recover from one file.

## Sections

Write the sections in this order. Omit an optional section when it does not apply.
Do not omit, reorder, or add anything else.

### Header

Project name and a short description for context.

### Entities

A table of `Entity | Is | Holds`, one row per thing the domain names. Keep `Is` to
a single clause. In `Holds`, list the fields another entity depends on, not the
full schema — the schema lives in code.

Use glossary terms for entity names, and match the names in the code.

### Relations

A table of `From | Relation | To | Cardinality | Note`. State cardinality on every
row, and mark a derived relation derived.

Write a relation with a composite source as one row: `Shape ⊕ Tuning ⊕ Capo →
renders-to → Note` states that three things must be present.

### Edges That Must Not Exist

A table. Give each row a relation a reader would reasonably assume, and say why it
is absent.

### Disambiguation *(optional)*

Write this section when a name carries more than one sense. Two shapes, both
common.

**One surface form, two parses.** State the rule that separates them, with one
example of each.

**One concept, two behaviors by origin.** The same property means one thing
arriving from configuration and another arriving from a request. State which
origin produces which behavior.

### Lifecycles *(optional)*

Write this section when entities have states. Give state progressions, one line
per entity. Put illegal transitions in Edges That Must Not Exist.

### Frame Conventions *(optional)*

Write this section when the domain has units, indices, or coordinates. State which
index is which, what a measurement is relative to, and where a convention flips.
Name deliberate redundancy along with what it buys.
