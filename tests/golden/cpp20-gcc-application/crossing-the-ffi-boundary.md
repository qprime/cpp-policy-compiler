cpp20-gcc-application › Crossing the FFI boundary

Read when: writing or touching the binding layer — names, validation, errors, absence, units, ownership, shared schemas.

## MUST — Names cross the language boundary unchanged

POL-0057

A function exposed across an FFI seam has the same name on both sides. No case
conversion at the binding, no `_impl` shim, no alternate spelling for the host
language's convention.

```
parse_config   in the host language
parse_config   in C++
```

This is what fixes the C++ naming case machine-wide rather than per project
(POL-0084). A per-project case choice makes unchanged crossing impossible, so
the naming rule is structural rather than cosmetic.

Where the host language's own convention differs, the binding does not adapt it.
The shared vocabulary wins on both sides, because the alternative is that the
same operation has two names and nobody can grep for it.

A renamed symbol breaks every form of navigation that spans the two languages at
once: search, call-graph tools, error messages, and the reader's memory. It also
makes the mapping something a person maintains, and a mapping maintained by hand
acquires entries that are wrong in one direction only. Keeping the name identical
costs a naming convention and removes the mapping entirely.

## MUST — The calling side validates before crossing

POL-0058

The caller validates its arguments before an FFI call. The callee may `assert`
cheaply; it does not re-validate defensively.

This is POL-0041 applied to a seam where the two sides have different type
systems. The validation belongs on the side that has the user's input, the
context to say what went wrong, and something useful to do about it.

An `assert` on the callee side is permitted and is not a second validation. It
documents the contract and fails loudly in a build that checks it, rather than
selecting a fallback.

Split validation across a seam produces two answers to what an invalid argument
means, and the far side's answer is always worse: it has the value and nothing
else. Its diagnostic cannot name the field the user actually supplied, and its
recovery cannot ask for a corrected one. Making the obligation one-sided also
makes it checkable, because there is exactly one place per call where the
argument was known to be good.

## MUST — Errors translate exactly once, at the binding layer

POL-0059

A C++ exception becomes a host-language error at the binding layer, and nowhere
else. No exception crosses the seam unhandled, and no layer below the binding
catches in order to re-throw a different type (POL-0053).

The host side does not re-wrap what it receives. Type and message are preserved
across the translation, so the four-part message (POL-0011) that was constructed
in C++ is the one the user reads.

```
C++            throw std::invalid_argument("RetryPolicy: max_attempts must be > 0, got 0")
binding layer  translate to the host language's exception, message intact
host           the same four parts, in the host language's error type
```

One translation point is what keeps the failure attributable. Each additional
wrap replaces a matchable type with a string and prepends a layer name, so the
top of the stack receives a message assembled from prefixes and no way to
identify where the failure came from. An unhandled exception crossing the seam is
worse than either: the behaviour is undefined, so a diagnosable failure becomes a
crash with no message at all.

## MUST — Absence maps to absence across the boundary

POL-0060

The optional mechanism on one side is the optional mechanism on the other. The
empty optional is the host language's null, and nothing else is.

Three things follow:

- NaN never crosses. A NaN arriving at the seam is a defect to investigate, not
  a missing value (POL-0013).
- An empty collection does not signal failure. It means the collection is empty.
- A sentinel does not become a null at the binding. If the C++ side produced a
  sentinel, the defect is on the C++ side (POL-0009).

The binding layer converts the representation and never the meaning. Where the
C++ standard predates a standard optional, the project's optional form is what
the binding maps, on the same terms.

A seam is where two value spaces meet, so it is where an overloaded value gets
its second chance to be misread. A `-1` translated to null at the binding gives
the host a clean-looking interface over a C++ signature that still admits the
sentinel everywhere else, which means the ambiguity survives and only the symptom
was hidden. Mapping absence to absence and nothing else keeps the seam a
translation rather than a repair.

## MUST — Unit conversion happens at the outer boundary, never at the FFI seam

POL-0061

A value arriving from user input or a parsed file is converted to the project's
internal unit there, at the outer edge. It crosses the FFI seam in that unit,
with its suffix intact (POL-0017), and the binding layer converts nothing.

```
user input / file  →  convert here, once
FFI seam           →  carry through unchanged
```

Converting at the seam is a category error. The seam is a language boundary, and
a unit is not a property of a language.

A conversion at the seam is invisible to both sides. The C++ side sees a value
in its own unit and the host side sees a value in its own unit, and neither
declaration says a factor was applied in between, so a value that takes a
different path into the system arrives unconverted and is indistinguishable.
Converting at the outer boundary puts the factor at the one place where the
value's unit is genuinely unknown, which is also the one place a wrong unit can
be reported to whoever supplied it.

## MUST — Ownership is explicit across the FFI boundary

POL-0062

| Crossing | Contract |
|----------|----------|
| By value | Copies. Neither side retains a reference to the other's storage. |
| By reference | Non-owning, with the lifetime documented at the declaration. |
| Transferring ownership out of C++ | `std::unique_ptr`, or by value. Never a raw pointer. |
| Passing a mutable host object in | Valid for the duration of the call only. C++ does not retain it. |

The host language's lifetime model does not extend into C++ and C++'s does not
extend into the host. Every crossing therefore states which of the four rows it
is, at the declaration, because neither runtime can work it out.

This is POL-0014 at the one boundary where the compiler cannot help. Inside C++,
a raw pointer is non-owning by rule and a `unique_ptr` says what it means; across
the seam the type is erased by the binding, so what survives is whatever the
declaration wrote down. A retained pointer to host storage is a use-after-free
whose two halves are in different languages, which puts it beyond the reach of
every tool that would otherwise find it.

## MUST — A structure shared across the boundary has one schema and one source of truth

POL-0063

Any structure both sides read or write — an intermediate representation, a
parsed model, a result payload — is defined once. The other side derives from
that definition rather than restating it.

A schema change is versioned and moves everything together, in one change:

1. define the new form in the schema
2. expose it across the FFI
3. document it
4. regenerate the goldens (POL-0071)

Adding an alternative to a shared structure follows the same four steps in the
same order. A definition that has moved without its goldens is a change nobody
can review, because the diff that would have shown its effect was not produced.

Two definitions of one structure agree on the day they are written and are edited
independently after. The disagreement does not fail to compile, because each side
compiles against its own copy; it appears as a field silently dropped or misread
at the seam, at runtime, on the inputs that exercise the new field. One
definition makes the mismatch a build failure, which is the only form of it that
is found before the data is wrong.

## SHOULD — The binding layer is a declared escape hatch

POL-0064

The binding layer converts, validates, and translates at the seam, and is
permitted the boilerplate that implies. It is the one place where boundary
ceremony is correct rather than a symptom.

What the escape covers: repeated conversion code, explicit validation of values
the C++ side would otherwise trust, raw-pointer handling dictated by a foreign
signature (POL-0046), and exception translation (POL-0059).

What it does not cover: business logic. A binding layer that computes anything is
no longer a binding layer, and the computation it acquired is now untested on
both sides.

Declare it as the boundary it is, in the file that implements it. The escape is
named so that the ceremony reads as deliberate rather than as an example to
follow.

Every rule the escape suspends was justified by an invariant established
elsewhere, and at the seam none of them has been established yet. Ceremony there
is the work of establishing them, which is why it is correct in exactly one file
and a defect in the next one over. Naming the file is what keeps the pattern from
spreading: without the declaration, the next author reads defensive conversion
code as the local convention and writes more of it inward.
