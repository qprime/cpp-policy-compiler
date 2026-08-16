cpp20-gcc-application › Naming

Read when: naming anything — case, operation verbs, return-contract prefixes, unit suffixes.

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
