# cpp20-gcc-application

- Standard: C++20
- Compiler: gcc
- Domain: application

Per-standard tables in these documents read against the declared standard above.

## Correct by construction beats correct by test

POL-0001 · CG P.4, CG P.5

The best defect is the one the type system refuses to compile. The second best
is the one a constructor rejects at the boundary. Tests confirm what the design
already guarantees; they are due diligence, not the correctness mechanism.

When two designs are otherwise equal, take the one that turns a class of mistake
into a compile error.

A codebase that relies on its test suite for correctness has moved the invariant
out of the code and into a process. That process runs after the code exists, if
it runs at all, and only over the cases someone thought to write. The compiler
runs against the code as written, every time.

## Failure modes are visible

POL-0002 · CG P.6, CG P.7

Errors are not swallowed. Invalid states are unrepresentable where possible and
rejected at construction where not. A function that cannot do what it was asked
says so; it does not return a plausible value.

A loud failure at the point of the mistake is always preferable to a quiet one
that survives.

A silent wrong answer is the worst possible failure, because nothing downstream
can tell it from a right one. Where output is consumed by another program, a
device, or a later build step rather than read by a person, there is no stage at
which the error becomes visible on its own. It is acted on, and the cost lands
far from the code that caused it.

## Ownership is obvious

POL-0003 · CG P.8

Who owns this memory, this resource, this lifetime is answerable from the
declaration alone. RAII by default: the owner is a type whose destructor
releases what it holds.

If answering the ownership question requires reading the body or tracing the
call graph, the declaration is the defect. Fix the declaration.

Ownership that is not stated in the declaration has to be inferred, and every
later edit re-infers it from whatever is visible at the time. An inference that
was correct once is not correct after the next change, which is how
use-after-free and double-release enter code that was right when it was written.

## Boring is a feature

POL-0004

Two language features rather than seven. Idiomatic rather than clever. Reach for
the construction a competent C++ engineer expects to find, not the one that
demonstrates the most about the language.

Where two spellings are equally correct, take the common one. Arbitrary
variation costs consistency and buys nothing.

Every feature reached for is a feature every later edit has to handle. Unusual
constructions widen the space of plausible continuations: the next change has
more ways to be written and fewer of them are consistent with what is already
there. Uniformity is what lets a large body of code be extended one piece at a
time without drift, and drift is not visible in any single line.

## Defensive at boundaries, trusting inside

POL-0005 · CG P.7

Validate at the outside edge: user input, file parsing, FFI, anything arriving
from a system whose guarantees you do not control. Past that edge, trust what
was established.

If a precondition is checked in three places, the fix is a type that establishes
it once, not a fourth check.

Scattered internal checks are a missing invariant, not thoroughness. They drift
the moment one site's fallback differs from another's, which turns one absent
invariant into two different behaviours for the same input.

## Express intent, not mechanism

POL-0006 · CG P.1, CG P.3, CG NL.1

The reader should see what the code means before how it works. A named operation
that says what it produces beats an inline block that computes it. A type that
names a constraint beats a comment stating it.

If the body must be opened to learn what a function is for, the name is the
defect. Where a comment would state what the code means, the name states it
instead.

Code that states its intent can be extended from its declaration. Code that
states only its mechanism has to be re-derived from its body before it can be
changed, and re-derivation is where wrong assumptions enter: the body shows what
the code does, never what it was required to do.

## Determinism is the default

POL-0007

Same input, same output, on every platform and every run. No dependence on
unordered-container iteration order, on address values, on uninitialized memory,
on wall-clock time, or on platform-dependent floating-point in output that is
compared.

If two runs over the same input can differ, that is a defect even when both
outputs are individually correct.

Non-determinism does not produce a wrong answer. It produces an answer that
cannot be checked. A result that differs between runs cannot be diffed against a
known-good one, so golden tests, reproducible builds, and any claim that a
change was safe all stop working at once.

## The compiler is your ally

POL-0008 · CG P.5

Strong types where they matter, `enum class` always, `[[nodiscard]]` where the
return value is the point, `constexpr` where possible, `noexcept` where
genuinely true, exhaustive dispatch that breaks compilation when a case is added.

Prefer the construction that makes a future mistake fail the build over the one
that makes it fail a test, and prefer either over the one that makes it fail in
the field.

The compiler is the one check present every time the code is built, on every
platform, with nothing to have been kept current and nobody to have remembered
to run it. Work moved into it is work that cannot be skipped.

## Map

- [Choosing a representation](choosing-a-representation.md) — deciding what type holds a piece of data — alternatives, absence, aggregates, inheritance, whether a thing becomes a type at all.
- [Building a class](building-a-class.md) — writing a type's mechanics — constructors, invariants, special members, `noexcept`, wrapper types.
- [Deciding ownership](deciding-ownership.md) — deciding who owns an allocation or resource and how the declaration says so.
- [Writing a function](writing-a-function.md) — writing a signature or body — parameters, decomposition, duplication, templates, `auto`.
- [Everyday declarations](everyday-declarations.md) — declaring anything — `const`, named constants, initialization, determinism.
- [Handling failure](handling-failure.md) — choosing what happens when an operation cannot do what it was asked.
- [Placing validation](placing-validation.md) — deciding where a check lives — boundaries validate, internals trust.
- [Structuring modules and layers](structuring-modules-and-layers.md) — laying out headers, includes, namespaces, dependency direction, or a threading model.
- [Naming](naming.md) — naming anything — case, operation verbs, return-contract prefixes, unit suffixes — and deciding whether to write a comment.
- [Crossing the FFI boundary](crossing-the-ffi-boundary.md) — writing or touching the binding layer — names, validation, errors, absence, units, ownership, shared schemas.
- [Writing tests](writing-tests.md) — writing or reviewing tests — what to test, what not to, goldens, round-trips, the framework.
- [Logging](logging.md) — emitting diagnostics from library or application code.
- [Coroutines](coroutines.md) — writing coroutines — lifetimes across suspension, captures, awaitables, deep chains. Vacuous below C++20.
- [Choosing a statement](choosing-a-statement.md) — shaping control flow — which loop, which selection, early returns, `switch` arms and fallthrough.
- [Writing an expression](writing-an-expression.md) — writing the line itself — casts, arithmetic and signedness, which standard-library facility to reach for, how text gets formatted.
- [Iterating a sequence](iterating-a-sequence.md) — walking a container — whether a loop is the right shape at all, how the element is bound, what may not change while iterating.
- [Running concurrently](running-concurrently.md) — a threading model exists and shared state has to be reached from more than one thread.
- [Build and tooling](build-and-tooling.md) — setting up or changing a project's build — warnings, sanitizers, static analysis, formatting, the standard declaration.
