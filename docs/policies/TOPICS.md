# Projection topics

The task-situation partition of the policy corpus. Each topic becomes one
topical document in the projection, and its *Read when* line becomes that
topic's entry in the always-loaded index.

Membership lists go under each *Read when* line, as a paragraph of policy ids.
`polc` fails while any topic has no members.

## Rules

Principles belong to no topic. They live in `principles.md`, which the map does
not route to; the procedure in the entry document sends the reader there for
what no trigger row matches.

A `trigger:` names the construct whose row a policy earns in its topic
document's table. Principles carry none, because they have no topic document to
hold the row.

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

POL-0017 POL-0025 POL-0057 POL-0065 POL-0066 POL-0067 POL-0068 POL-0090
POL-0093 POL-0097 POL-0098 POL-0105 POL-0106 POL-0107 POL-0108 POL-0198
POL-0210 POL-0222 POL-0224 POL-0229

### Building a class

Read when: writing a type's mechanics — constructors, invariants, special
members, `noexcept`, wrapper types.

POL-0058 POL-0059 POL-0060 POL-0063 POL-0064 POL-0069 POL-0070 POL-0071
POL-0072 POL-0073 POL-0074 POL-0075 POL-0076 POL-0077 POL-0078 POL-0079
POL-0080 POL-0081 POL-0082 POL-0083 POL-0084 POL-0085 POL-0086 POL-0087
POL-0088 POL-0089 POL-0091 POL-0092 POL-0094 POL-0095 POL-0096 POL-0099
POL-0100 POL-0101

Cross-reference: POL-0018

### Deciding ownership

Read when: deciding who owns an allocation or resource and how the declaration
says so.

POL-0021 POL-0022 POL-0040 POL-0044 POL-0045 POL-0046 POL-0109 POL-0110
POL-0111 POL-0112 POL-0113 POL-0114 POL-0115 POL-0116

### Writing a function

Read when: writing a signature or body — parameters, decomposition,
duplication, templates, `auto`.

POL-0014 POL-0024 POL-0029 POL-0033 POL-0034 POL-0035 POL-0036 POL-0037
POL-0038 POL-0039 POL-0041 POL-0042 POL-0047 POL-0048 POL-0049 POL-0050
POL-0051 POL-0052 POL-0053 POL-0054 POL-0055 POL-0061 POL-0102 POL-0103
POL-0118 POL-0119 POL-0195 POL-0196 POL-0197 POL-0199 POL-0200 POL-0201
POL-0202 POL-0203 POL-0205 POL-0206 POL-0207 POL-0208 POL-0209 POL-0212
POL-0213 POL-0214 POL-0215 POL-0231 POL-0232

### Everyday declarations

Read when: declaring anything — `const`, named constants, initialization,
determinism.

POL-0015 POL-0023 POL-0030 POL-0062 POL-0104 POL-0120 POL-0121 POL-0123
POL-0124 POL-0125 POL-0126 POL-0127 POL-0128 POL-0129 POL-0133 POL-0134
POL-0152 POL-0204

### Handling failure

Read when: choosing what happens when an operation cannot do what it was asked.

POL-0032 POL-0183 POL-0184 POL-0185 POL-0186 POL-0187 POL-0188 POL-0189
POL-0190 POL-0191 POL-0192 POL-0193 POL-0228

Cross-reference: POL-0058

### Placing validation

Read when: deciding where a check lives — boundaries validate, internals trust.

POL-0018 POL-0019 POL-0020 POL-0194

### Structuring modules and layers

Read when: laying out headers, includes, namespaces, dependency direction, or a
threading model.

POL-0011 POL-0016 POL-0028 POL-0217 POL-0218 POL-0219 POL-0239

### Naming

Read when: naming anything — case, operation verbs, return-contract prefixes,
unit suffixes — and deciding whether to write a comment.

POL-0122

### Crossing the FFI boundary

Read when: writing or touching the binding layer — names, validation, errors,
absence, units, ownership, shared schemas.

POL-0026 POL-0027 POL-0043 POL-0211 POL-0216 POL-0230 POL-0233 POL-0234
POL-0235 POL-0236 POL-0237 POL-0238

### Writing tests

Read when: writing or reviewing tests — what to test, what not to, goldens,
round-trips, the framework.

POL-0240 POL-0241 POL-0242 POL-0243 POL-0244 POL-0245 POL-0246 POL-0247

### Logging

Read when: emitting diagnostics from library or application code.

POL-0225 POL-0226 POL-0248

### Real-time loops

Read when: writing code under a deadline — scan loops, audio callbacks,
interrupt handlers. The whole topic is gated by the realtime domain.

POL-0161 POL-0162

Cross-reference: POL-0190

### Coroutines

Read when: writing coroutines — lifetimes across suspension, captures,
awaitables, deep chains. Vacuous below C++20.

POL-0179 POL-0180 POL-0181 POL-0182

### Choosing a statement

Read when: shaping control flow — which loop, which selection, early returns,
`switch` arms and fallthrough.

POL-0056 POL-0143 POL-0144 POL-0145 POL-0147 POL-0149 POL-0150 POL-0151
POL-0153

Cross-reference: POL-0146

### Writing an expression

Read when: writing the line itself — casts, arithmetic and signedness, which
standard-library facility to reach for, how text gets formatted.

POL-0013 POL-0117 POL-0130 POL-0131 POL-0132 POL-0135 POL-0136 POL-0137
POL-0138 POL-0140 POL-0141 POL-0142 POL-0154 POL-0155 POL-0220 POL-0221
POL-0223 POL-0227

### Iterating a sequence

Read when: walking a container — whether a loop is the right shape at all, how
the element is bound, what may not change while iterating.

POL-0139 POL-0146 POL-0148

Cross-reference: POL-0128

### Running concurrently

Read when: a threading model exists and shared state has to be reached from more
than one thread.

POL-0163 POL-0164 POL-0165 POL-0166 POL-0167 POL-0169 POL-0170 POL-0171
POL-0172 POL-0173 POL-0174 POL-0175 POL-0176 POL-0177 POL-0178

### Build and tooling

Read when: setting up or changing a project's build — warnings, sanitizers,
static analysis, formatting, the standard declaration.

POL-0009 POL-0012

### Optimizing

Read when: deciding whether to make code faster, and what to change once a
measurement says where the time goes.

POL-0010 POL-0031 POL-0156 POL-0157 POL-0158 POL-0159 POL-0160

Cross-reference: POL-0030

## Standing decisions

- Placing validation stays separate from Handling failure. They answer
  different questions: where a check lives, versus what happens on failure.
- Large topics stay whole. A topic is not pre-split on size alone.
- Real-time loops is the domain axis's first whole-topic customer. Coroutines is
  the topic-level face of the gate-or-content question in [README.md](README.md),
  since its subject does not exist below C++20.
