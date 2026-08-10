---
id: POL-0039
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 3: exceptions are permitted at module boundaries"
  - source: cpp-convention/conventions.md
    locator: "Divergences: CG E.2, CG I.10"
  - source: cpp-convention/mechanisms.md
    locator: "§5 Failure, exception-free modules"
    upstream: ["CG E.25", "CG E.26", "CG E.27"]
---

# Exceptions are permitted at module boundaries

An exception is for a genuinely exceptional condition raised at a module
boundary: allocation failure, invariant violation, unrecoverable corruption. A
routine fallible operation returns a result type instead (POL-0031).

Three named escapes bound where exceptions may appear:

- **Forbidden in real-time loops.** Their timing is not deterministic
  (POL-0076).
- **Never cross an FFI boundary un-translated.** Translation happens exactly
  once, at the binding layer (POL-0059).
- **`-fno-exceptions` is permitted per module** when latency, binary size, or an
  FFI target justifies it, declared in that module's top-level header.

A module compiled without exceptions follows the exception-free discipline:
simulate RAII for resource management, fail fast where that is the right answer,
and use error codes systematically — one convention for the module, stated where
its header states the compilation mode.

This is narrower than the general position that exceptions are the error-handling
mechanism, and the narrowing is deliberate. That position assumes neither a
latency deadline nor a foreign-language seam, and both are present here. Where
neither applies, an exception at a module boundary is the right mechanism and
carries no apology.
