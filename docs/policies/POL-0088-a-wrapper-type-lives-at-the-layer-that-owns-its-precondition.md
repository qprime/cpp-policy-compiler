---
id: POL-0088
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Dependency Direction: a wrapper type used by several layers"
---

# A wrapper type lives at the layer that owns its precondition

Where several layers use a wrapper type (POL-0027), it is defined at the layer
that establishes the precondition, not at the layer that consumes the value.

The owning layer is the one that can produce the type: the one holding the
validation, the parsing, or the invariant that makes the conversion possible.
Consumers depend on it in the permitted direction (POL-0018).

Where two layers both appear to establish it, the precondition is being checked
twice and one of the checks is redundant (POL-0045). Resolve that before placing
the type.

Placing the type with a consumer inverts the dependency the moment a second
consumer appears, because the second one has no reason to depend on the first.
The producing layer then either includes downward to construct the type or hands
back an unvalidated value, and both undo the guarantee the wrapper existed for.
Placing it with the producer makes the type available to every consumer along
the direction includes already flow, so adding a consumer costs nothing
structural.
