cpp20-gcc-application › Naming

Read when: naming anything — case, operation verbs, return-contract prefixes, unit suffixes — and deciding whether to write a comment.

## MUST — Dimensioned values carry their unit in the name

POL-0017 · CG I.4, CG NL.19

A value with a physical or conventional dimension states that dimension as a
name suffix: `timeout_ms`, `size_bytes`, `rate_hz`, `angle_deg`, `width_px`. At
every interface, without exception.

The suffix names the unit, not the quantity: `_ms` and not `_time`. A parameter,
a member, a return value, and a constant naming the same quantity all carry the
same suffix, so a conversion is visible as a change of suffix rather than
inferred from arithmetic.

A ratio or a count has no unit and takes none. Where a value genuinely carries
two units, the name carries both in the order they divide: `rate_bytes_per_sec`.

The suffix is not a substitute for a strong type, and it is also not a step
toward one. POL-0038 states when a distinct type earns its cost; below that bar
the suffix is the whole mechanism.

A dimensioned quantity has no compiler-visible dimension, so a millisecond
assigned to a seconds parameter compiles, runs, and produces an answer that is
wrong by three orders of magnitude. Nothing downstream can detect it, because
every value involved is a legal instance of its type. The name is the only place
the unit can live, which is why it is required at the interface rather than
recommended inside it.

## MUST — Naming case is fixed, not a per-project choice

POL-0084 · CG NL.5, CG NL.8, CG NL.9, CG NL.10

| Kind | Case | Example |
|------|------|---------|
| Functions, variables, parameters, members | `snake_case` | `parse_config`, `timeout_ms` |
| Private data members | `snake_case_`, trailing underscore | `max_attempts_` |
| Types: class, struct, enum, alias | `PascalCase` | `RetryPolicy`, `CompactParams` |
| Enumerators | `PascalCase` | `CompactMode::Incremental` |
| Constants at namespace scope | `kPascalCase` | `kMinFillRatio` |
| Macros | `ALL_CAPS`, project-prefixed, and avoid macros | `PROJ_ASSERT` |
| Namespaces | `snake_case`, nested by layer | `proj::store` |
| Files | `snake_case`, `.hpp` and `.cpp` | `compact.cpp` |

`ALL_CAPS` is for macros and nothing else. Type information is not encoded in
names: no Hungarian prefixes, no `_ptr` suffix on a pointer, no `_t` on a type.

`.hpp` rather than `.h` for a C++ header, so a C++ header is distinguishable
from a C header at a glance in a tree that contains both.

The case is fixed rather than recommended because names must cross the FFI seam
unchanged (POL-0057), and unchanged crossing is impossible if each side picks
its own case. That makes this structural rather than cosmetic: a per-project
choice does not merely produce variety, it makes a whole class of rule
unstatable. The upstream guidance offers underscore style as a preference; here
it is a requirement, and the requirement is what the preference cannot supply.

## MUST — Operation verbs are a fixed vocabulary

POL-0085

Same verb, same operation, everywhere and in every language the project spans.

| Verb | Meaning | Example |
|------|---------|---------|
| `parse_*` | Text or bytes to structured data | `parse_config` |
| `format_*` | Structured data to text | `format_output` |
| `resolve_*` | Simplify structure, expand references | `resolve_imports` |
| `*_to_*` | Convert between typed representations | `ast_to_ir` |
| `validate_*` | Check correctness; throw or return an error | `validate_bounds` |
| `build_*` | Construct a complex object from parts | `build_pipeline` |
| `load_*` | Read from disk or an external source | `load_config` |
| `write_*` | Emit machine or file output | `write_report` |
| `render_*` | Emit visual output | `render_diagram` |
| `expand_*` | Parameterized instantiation | `expand_template` |
| `plan_*` | Compute an execution sequence | `plan_execution` |

Where an operation is one of these, it uses that verb and no synonym. Where it
is not, the verb is new, and adding one is a decision about the vocabulary
rather than about the function.

A verb chosen per function is a verb that carries no information, because the
reader cannot tell a deliberate distinction from a synonym somebody preferred
that day. `load_config` beside `read_config` beside `get_config` reads as three
different operations and is usually one. Fixing the vocabulary makes the verb
part of the type: seeing `parse_` says the input is text and the output is
structure, without opening anything. It is also what makes the corpus greppable,
which is the only way to find every conversion in a tree nobody has read.

## MUST — A name prefix states the return contract

POL-0086

| Pattern | Returns |
|---------|---------|
| `is_*` / `has_*` | `bool` |
| `try_*` / `try_from` | An optional or a result. Never throws |
| `get_*` | An accessor that cannot fail; the precondition is the caller's |
| `find_*` | An optional or an iterator |
| `make_*` | Constructs a value |

The contract runs both ways. A function named `try_*` that throws is a defect,
and so is a fallible operation named `get_*`.

`try_from` is the non-throwing companion to a validating constructor
(POL-0022) and to a wrapper type's conversion (POL-0027). Where one exists, this
is its name.

The prefix is the part of a signature a reader sees before the return type, and
at a call site it is often the only part they see. A `find_` that returns an
optional and a `get_` that cannot fail need different handling at every call, so
encoding the difference in the prefix means the handling is chosen while writing
rather than after a compile error. The rule earns most where the return type is
elided (POL-0050): with `auto` on the left, the prefix is all the reader has.

## MUST — A comment states what the code cannot

POL-0112 · CG NL.1

```cpp
// Right: an identity the reader cannot derive from the expression.
// Shoelace formula; sign of the result gives the winding direction.
const auto area2 = cross(a, b) + cross(b, c) + cross(c, a);

// Right: a load-bearing assumption the types do not carry.
// Caller holds scan_mutex_; this runs inside the scan window.
void append_trace(const Fault& f);
```

The three cases are a non-obvious identity or derivation, an assumption the
code depends on and the types do not express, and the reason for a choice that
otherwise reads as arbitrary.

No docstring block on every function, and no running prose narrating the next
few lines. Volume trains the reader to skip comments, which costs the few that
carry something.

Everything else the name carries instead, which is POL-0006 applied to the
comment case. A comment is the fallback for what naming cannot reach, so its
value depends entirely on being rare: a reader who has learned that comments
here are load-bearing will read them, and a reader who has learned they restate
the code will skip the one that mattered.

## NEVER — Never write a comment that restates the code

POL-0113 · CG NL.2

```cpp
// Never.
// Increment the retry count.
++retries;

// Never. The signature already says all of this.
/// @brief Gets the diameter.
/// @return The diameter.
double diameter_mm() const;
```

Delete it. Where the line genuinely needs explaining, the explanation is a
name or a function (POL-0030), not a sentence above it.

A restating comment doubles the edit surface for no information, and the two
copies drift on the first change that touches one of them. What remains is a
false statement sitting immediately beside a true one, with nothing marking
which is which — and the comment is what a reader in a hurry reads.

Generated docstring blocks are the same defect at scale. They pass any
documentation-coverage check while telling the reader nothing the declaration
did not already say (POL-0112).
