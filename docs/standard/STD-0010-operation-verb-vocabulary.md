---
id: STD-0010
group: names
enforced_by: review
review_trigger: "an operation name uses a verb outside the project vocabulary"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Naming Vocabulary"
---

# An operation is named from the fixed verb vocabulary

| Verb | Meaning | Example |
|------|---------|---------|
| `parse_*` | Text or bytes → structured data | `parse_config` |
| `format_*` | Structured data → text | `format_output` |
| `resolve_*` | Simplify structure, expand references | `resolve_layout` |
| `*_to_*` | Convert between typed representations | `ast_to_ir` |
| `validate_*` | Check correctness; throw or return an error | `validate_bounds` |
| `build_*` | Construct a complex object from parts | `build_pipeline` |
| `load_*` | Read from disk or an external source | `load_config` |
| `write_*` | Emit machine or file output | `write_report` |
| `render_*` | Emit visual output | `render_diagram` |
| `expand_*` | Parameterized instantiation | `expand_template` |
| `plan_*` | Compute an execution sequence | `plan_pocket` |

A new verb is added here before it is used, not after.

The vocabulary is identical in the Python convention, so a name means the same
operation on both sides of the FFI boundary.
