# INVARIANTS.md

Artifact: `INVARIANTS.md` at the repository root. Earned when the project has
rules whose enforcement it can name — installed in code, or committed in a
specification the project has adopted.

## Sections

Write the sections in this order. Omit an optional section when it does not apply.
Do not omit, reorder, or add anything else.

### Header

Project name and a short description for context.

### Summary Table

Every invariant in the file, as a table. Give each row the ID, the name, and the
type.

### Invariants

One entry per invariant, in ID order. Open each entry with a heading carrying its
ID, its SCREAMING_SNAKE name, and its type, then state the rule.

Then give its fields:

| Field | When |
|---|---|
| **Why** | Always. What the rule protects. |
| **Enforcement** | Always. The assertion, frozen type, required field, test, or gate that stops the violation. |
| **Evidence** | Once the enforcement exists. Name a symbol, not a line. |
| **Pending** | While the enforcement is decided but not yet built. Replace it with Evidence when it lands. |

Type the invariant by what violating it costs:

| Type | Cost of violation |
|---|---|
| **HARD** | Correctness breaks now. |
| **STRUCTURAL** | Nothing breaks immediately; changing it requires a coordinated migration. |

Add either orthogonal flag where it applies. **REGRESSION TRAP** carries the
commit where someone violated the rule and reverted. **SAFETY** means violations
corrupt data, damage hardware, or harm people.

Past roughly twenty entries, split this section into
`docs/invariants/<subsystem>.md` and match the ID prefixes to the file names. Keep
the Summary Table in `INVARIANTS.md` as the index.
