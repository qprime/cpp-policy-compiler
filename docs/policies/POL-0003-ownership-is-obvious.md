---
id: POL-0003
kind: principle
precedence: 3
attribution:
  - source: cpp-convention/conventions.md
    locator: "Values #3"
    upstream: ["CG P.8"]
---

# Ownership is obvious

Who owns this memory, this resource, this lifetime is answerable from the
declaration alone. RAII by default: the owner is a type whose destructor
releases what it holds.

If answering the ownership question requires reading the body or tracing the
call graph, the declaration is the defect. Fix the declaration.

Ownership that is not stated in the declaration has to be inferred, and every
later edit re-infers it from whatever is visible at the time. An inference that
was correct once is not correct after the next change, which is how
use-after-free and double-release enter code that was right when it was written.
