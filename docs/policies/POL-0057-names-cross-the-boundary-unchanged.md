---
id: POL-0057
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "FFI Conventions: names cross unchanged"
---

# Names cross the language boundary unchanged

A function exposed across an FFI seam has the same name on both sides. No case
conversion at the binding, no `_impl` shim, no alternate spelling for the host
language's convention.

```
parse_config   in the host language
parse_config   in C++
```

This is what fixes the C++ naming case machine-wide rather than per project
(POL-0084). A per-project case choice makes unchanged crossing impossible, so
the naming rule is structural rather than cosmetic.

Where the host language's own convention differs, the binding does not adapt it.
The shared vocabulary wins on both sides, because the alternative is that the
same operation has two names and nobody can grep for it.

A renamed symbol breaks every form of navigation that spans the two languages at
once: search, call-graph tools, error messages, and the reader's memory. It also
makes the mapping something a person maintains, and a mapping maintained by hand
acquires entries that are wrong in one direction only. Keeping the name identical
costs a naming convention and removes the mapping entirely.
