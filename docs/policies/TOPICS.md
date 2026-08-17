# Projection topics

The task-situation partition of the policy corpus. Each topic becomes one
topical document in the projection, and its *Read when* line becomes that
topic's entry in the always-loaded index.

Membership lists go under each *Read when* line, as a paragraph of policy ids.
They are empty pending the corpus rebuild, and `polc` fails while any topic has
no members.

## Rules

Principles belong to no topic. They are index-level content, always loaded.

Membership is single. A policy that matters in a second situation gets a
`Cross-reference:` line there, never a second entry, because two entries are two
places to edit and a reader cannot tell which one is canonical. The compiler
treats a policy in two topics as a build error.

Totality is enforced. Every non-principle policy appears in exactly one topic,
and every id resolves.

Topic membership is a corpus fact rather than a format decision. A new policy
joins a topic or forces a new one, and either lands as an edit to this file.
A topic that stops answering a single question splits here, not in the compiler.

## Topics

### Choosing a representation

Read when: deciding what type holds a piece of data — alternatives, absence,
aggregates, inheritance, whether a thing becomes a type at all.

### Building a class

Read when: writing a type's mechanics — constructors, invariants, special
members, `noexcept`, wrapper types.

### Deciding ownership

Read when: deciding who owns an allocation or resource and how the declaration
says so.

### Writing a function

Read when: writing a signature or body — parameters, decomposition,
duplication, templates, `auto`.

### Everyday declarations

Read when: declaring anything — `const`, named constants, initialization,
determinism.

### Handling failure

Read when: choosing what happens when an operation cannot do what it was asked.

### Placing validation

Read when: deciding where a check lives — boundaries validate, internals trust.

### Structuring modules and layers

Read when: laying out headers, includes, namespaces, dependency direction, or a
threading model.

### Naming

Read when: naming anything — case, operation verbs, return-contract prefixes,
unit suffixes — and deciding whether to write a comment.

### Crossing the FFI boundary

Read when: writing or touching the binding layer — names, validation, errors,
absence, units, ownership, shared schemas.

### Writing tests

Read when: writing or reviewing tests — what to test, what not to, goldens,
round-trips, the framework.

### Logging

Read when: emitting diagnostics from library or application code.

### Real-time loops

Read when: writing code under a deadline — scan loops, audio callbacks,
interrupt handlers. The whole topic is gated by the realtime domain.

### Coroutines

Read when: writing coroutines — lifetimes across suspension, captures,
awaitables, deep chains. Vacuous below C++20.

### Choosing a statement

Read when: shaping control flow — which loop, which selection, early returns,
`switch` arms and fallthrough.

### Writing an expression

Read when: writing the line itself — casts, arithmetic and signedness, which
standard-library facility to reach for, how text gets formatted.

### Iterating a sequence

Read when: walking a container — whether a loop is the right shape at all, how
the element is bound, what may not change while iterating.

### Running concurrently

Read when: a threading model exists and shared state has to be reached from more
than one thread.

### Build and tooling

Read when: setting up or changing a project's build — warnings, sanitizers,
static analysis, formatting, the standard declaration.

## Standing decisions

- Placing validation stays separate from Handling failure. They answer
  different questions: where a check lives, versus what happens on failure.
- Large topics stay whole. A topic is not pre-split on size alone.
- Real-time loops is the domain axis's first whole-topic customer. Coroutines is
  the topic-level face of the gate-or-content question in [README.md](README.md),
  since its subject does not exist below C++20.
