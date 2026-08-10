---
id: POL-0085
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Naming vocabulary: verb table"
---

# Operation verbs are a fixed vocabulary

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
