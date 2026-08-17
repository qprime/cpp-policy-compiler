# Projection topics

The task-situation partition of the policy corpus, derived 2026-08-15 from the
full 93-policy corpus. This is the authored source for the projection's Tier 2
structure: each topic becomes one topical document, its *read when* line is that
topic's entry in the Tier 1 map, and the compiler enforces totality — every
non-principle policy appears in exactly one topic, every id resolves.

Principles (POL-0001 through POL-0008) belong to no topic. They are Tier 1
content.

Membership is single. A policy that matters in a second situation gets a
one-line cross-reference there, never a second entry, because two entries are
two places to edit and a reader cannot tell which one is canonical. The
compiler treats a policy in two topics as a build error.

## Topics

### Choosing a representation

Read when: deciding what type holds a piece of data — alternatives, absence,
aggregates, inheritance, whether a thing becomes a type at all.

POL-0009, POL-0013, POL-0033, POL-0034, POL-0037, POL-0038, POL-0042,
POL-0043, POL-0044, POL-0103, POL-0104, POL-0150, POL-0155, POL-0156,
POL-0160, POL-0161

### Building a class

Read when: writing a type's mechanics — constructors, invariants, special
members, `noexcept`, wrapper types.

POL-0015, POL-0021, POL-0022, POL-0025, POL-0027, POL-0051, POL-0120,
POL-0121, POL-0122, POL-0123, POL-0125, POL-0126, POL-0136, POL-0144,
POL-0145, POL-0146, POL-0147, POL-0148, POL-0149, POL-0166, POL-0167

### Deciding ownership

Read when: deciding who owns an allocation or resource and how the declaration
says so.

POL-0014, POL-0024, POL-0048, POL-0127, POL-0128, POL-0168

### Writing a function

Read when: writing a signature or body — parameters, decomposition,
duplication, templates, `auto`.

POL-0016, POL-0023, POL-0029, POL-0030, POL-0035, POL-0040, POL-0046,
POL-0047, POL-0050, POL-0052, POL-0054, POL-0056, POL-0114, POL-0115,
POL-0116, POL-0129, POL-0130, POL-0132, POL-0135, POL-0151, POL-0154,
POL-0159

Cross-reference: POL-0017 (unit suffixes, homed in Naming).

### Everyday declarations

Read when: declaring anything — `const`, named constants, initialization,
determinism.

POL-0010, POL-0019, POL-0020, POL-0026, POL-0096, POL-0097, POL-0153,
POL-0157, POL-0165

### Handling failure

Read when: choosing what happens when an operation cannot do what it was
asked.

POL-0011, POL-0031, POL-0032, POL-0039, POL-0053, POL-0055, POL-0163,
POL-0164

### Placing validation

Read when: deciding where a check lives — boundaries validate, internals
trust.

POL-0036, POL-0041, POL-0045

### Structuring modules and layers

Read when: laying out headers, includes, namespaces, dependency direction, or
a threading model.

POL-0018, POL-0028, POL-0049, POL-0087, POL-0088, POL-0124, POL-0137,
POL-0162

### Naming

Read when: naming anything — case, operation verbs, return-contract prefixes,
unit suffixes — and deciding whether to write a comment.

POL-0017, POL-0084, POL-0085, POL-0086, POL-0112, POL-0113, POL-0152

### Crossing the FFI boundary

Read when: writing or touching the binding layer — names, validation, errors,
absence, units, ownership, shared schemas.

POL-0057, POL-0058, POL-0059, POL-0060, POL-0061, POL-0062, POL-0063,
POL-0064

### Writing tests

Read when: writing or reviewing tests — what to test, what not to, goldens,
round-trips, the framework.

POL-0065, POL-0066, POL-0067, POL-0068, POL-0069, POL-0070, POL-0071,
POL-0072

### Logging

Read when: emitting diagnostics from library or application code.

POL-0073, POL-0074, POL-0075

### Real-time loops

Read when: writing code under a deadline — scan loops, audio callbacks,
interrupt handlers. The whole topic is gated by the realtime domain.

POL-0012, POL-0076, POL-0077, POL-0078, POL-0079

### Coroutines

Read when: writing coroutines — lifetimes across suspension, captures,
awaitables, deep chains. Vacuous below C++20.

POL-0080, POL-0081, POL-0082, POL-0083

### Choosing a statement

Read when: shaping control flow — which loop, which selection, early returns,
`switch` arms and fallthrough.

POL-0117, POL-0118, POL-0119

### Writing an expression

Read when: writing the line itself — casts, arithmetic and signedness, which
standard-library facility to reach for, how text gets formatted.

POL-0094, POL-0095, POL-0101, POL-0102, POL-0109, POL-0110, POL-0111,
POL-0131, POL-0134, POL-0169, POL-0170, POL-0171

### Iterating a sequence

Read when: walking a container — whether a loop is the right shape at all, how
the element is bound, what may not change while iterating.

POL-0098, POL-0099, POL-0100, POL-0133

### Running concurrently

Read when: a threading model exists and shared state has to be reached from
more than one thread.

POL-0105, POL-0106, POL-0107, POL-0108, POL-0138, POL-0139, POL-0140,
POL-0141, POL-0142, POL-0143

Cross-reference: POL-0049 (whether a threading model is warranted at all,
homed in Structuring modules and layers).

### Build and tooling

Read when: setting up or changing a project's build — warnings, sanitizers,
static analysis, formatting, the standard declaration.

POL-0089, POL-0090, POL-0091, POL-0092, POL-0093, POL-0158, POL-0172

## Rulings

Recorded at ratification, 2026-08-15:

- Large topics stay whole. Writing a function (12 entries) and the two type
  topics are not pre-split; a topic that stops answering one question splits
  into two topics here, which is an edit to this file rather than a compiler
  feature.
- POL-0019 homes with Everyday declarations, beside its nearest neighbours
  (initialize at declaration, `const` forces it), not with the tooling that
  merely catches violations of it.
- POL-0017 homes in Naming — it is a rule about what a name contains — with a
  cross-reference from Writing a function, its most frequent application site.
- Placing validation stays a separate topic from Handling failure. They answer
  different questions: where a check lives versus what happens on failure.

## Notes

- Every anti-pattern lands in the same topic as at least one of its
  replacements, so adjacency at render time needs no cross-topic machinery.
  The two exceptions are POL-0050 and POL-0055, whose replacements are
  principles and therefore always loaded. POL-0045 co-locates with POL-0041;
  its other replacement POL-0022 sits in Building a class.
- Real-time loops is the domain axis's first whole-topic customer. Coroutines
  is the topic-level face of the open gate-or-content question recorded in
  [README.md](README.md): its subject does not exist below C++20, so whether
  the projection omits the document or the entry decides that question.
- Topic count and membership are corpus facts, not format: new policies join a
  topic or force a new one, and either lands as an edit to this file.
