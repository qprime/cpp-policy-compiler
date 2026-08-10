---
id: POL-0032
kind: pattern
attribution:
  - source: cpp-convention/conventions.md
    locator: "Failure semantics by layer"
---

# Failure becomes less fatal moving outward

The layer a failure occurs in decides what happens to it. Parsers are strict;
orchestrators tolerate per-item failure and stay strict about safety.

| Layer | On failure |
|-------|-----------|
| FFI boundary | Translate into the host language's mechanism. Never let one cross unhandled (POL-0059). |
| Module public API | Return a result type for recoverable failure; throw only for invariant violations. |
| Internal helpers | Trust contracts. Input was validated upstream; `assert` cheaply where defensible. |
| Real-time loop | Record in a pre-allocated trace and continue. Never throw (POL-0076, POL-0077). |
| Real-time loop boundary | Inspect the accumulated trace and decide whether to halt. |

Read the table as a question about position, not severity. The same failing
operation gets a different treatment depending on which layer called it, and the
layer is what the author knows without looking anything up.

A uniform failure policy is wrong at both ends. Applied at the strictness of a
parser, an orchestrator aborts a whole run for one bad item; applied at the
tolerance of an orchestrator, a parser accepts malformed input and hands the
defect downstream where its origin is gone. Tying the treatment to the layer
puts the decision where the information about the caller's options actually is.
