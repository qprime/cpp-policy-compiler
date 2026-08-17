# conventions.md additions

Temporary. Candidate policies drawn from
[conventions.md](../source/cpp-convention/conventions.md) that
[CG-WORKLIST.md](CG-WORKLIST.md) does not already cover. Fill the **Policy**
column as each is written; strike rows that will not become policies.

The **CG** column says how the candidate stands to the Core Guidelines:

- **none** — the CG has no rule on the subject
- **extends** — a CG rule exists and this adds a threshold, escape, or mechanism the CG leaves open
- **diverges** — a CG rule exists and this takes a different position

Rows marked *ours* in conventions.md, plus every uncited claim, are the input to
this list. 69 candidates.

## Tier 1

| Candidate | CG | Policy |
|-----------|----|--------|
| Errors carry a four-part message: what failed, what field, what constraint, actual value | none | |
| Dependency direction holds; includes flow one way through the layer stack | none | |
| Determinism extends to output: no unordered-container iteration order, no platform-dependent floating point in golden output | extends [Ideally, a program should be statically type safe](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-typesafe) (P.4), [Always initialize an object](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-always) (ES.20) | |

## Tier 3 escapes

| Candidate | CG | Policy |
|-----------|----|--------|
| Dimensioned scalars stay primitives with unit-suffixed names; a strong typedef requires two confusable units at a boundary *and* arithmetic that does not flow through the type | diverges [Make interfaces precisely and strongly typed](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-typed) (I.4) | |
| Exceptions are permitted at module boundaries, forbidden in real-time loops, never cross FFI un-translated; `-fno-exceptions` is per-module and declared in that module's top-level header | diverges [Throw an exception to signal that a function can't perform its assigned task](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-throw) (E.2), [Use exceptions to signal a failure to perform a required task](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-except) (I.10) | |
| The FFI layer is a declared escape hatch from validate-at-the-boundary and is permitted the boilerplate that implies | extends [Catch run-time errors early](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-early) (P.7) | |

## Patterns

| Candidate | CG | Policy |
|-----------|----|--------|
| A type with a validating constructor gets a static `try_from` that delegates to the constructor rather than duplicating the validation | none | |
| More than four parameters triggers a params struct regardless of types; two adjacent same-type parameters trigger it regardless of count | extends [Keep the number of function arguments low](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-nargs) (I.23), [Avoid adjacent parameters that can be invoked by the same arguments in either order with different meaning](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-unrelated) (I.24) | |
| Ordered mathematical arguments are the named escape: `lerp(a, b, t)`, `clamp(v, lo, hi)`, `atan2(y, x)` | extends [Keep the number of function arguments low](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-nargs) (I.23) | |
| Naming the parameters and giving them distinct types are alternative ways to satisfy the adjacent-parameter rule; both are not required | extends [Avoid adjacent parameters that can be invoked by the same arguments in either order with different meaning](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-unrelated) (I.24) | |
| Include guards are named `PROJECT_COMPONENT_FILE_HPP`; `#pragma once` is a vendor extension and is not used | extends [Use `#include` guards for all header files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-guards) (SF.8) | |
| Scalar preconditions get no wrapper type; wrappers are for structural preconditions | none | |
| Repeated asserts of the same precondition are a missing wrapper type | extends [State preconditions (if any)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-pre) (I.5) | |
| Silent partial output is never an acceptable failure mode | none | |
| Failure becomes less fatal moving outward: FFI translates, module API returns a result, internals trust, the real-time loop records and continues, the loop boundary inspects the trace | none | |

## Decision procedures

| Candidate | CG | Policy |
|-----------|----|--------|
| A thing becomes a type by an ordered test: invariant, then structural precondition, then fixed alternatives, then values travelling together, then confusable-without-arithmetic, else a primitive with a unit-suffixed name | none | |
| A strong typedef is not introduced where arithmetic flows through the value; a partial units type is ceremony without safety | diverges [Make interfaces precisely and strongly typed](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-typed) (I.4) | |
| Inheritance waits for the second concrete case; with one in hand, write the function | none | |

## Traps

| Candidate | CG | Policy |
|-----------|----|--------|
| A variant visitor carries one overload per alternative and never a generic `[](auto&&)` fallback | none | |
| A non-owning view is never stored as a member; it is an owning member or a call-duration parameter | none | |
| Every type is single-threaded by contract until a threading model is declared; a mutex member without one is removed | diverges [Assume that your code will run as part of a multi-threaded program](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-multi) (CP.1) | |
| `auto` is for a type obvious from the right-hand side or unspellable, not where the type is the load-bearing fact | diverges [Use `auto` to avoid redundant repetition of type names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-auto) (ES.11) | |
| `(void)param;` is allowed only where an override or interface mandates the signature; on a leaf function the parameter is deleted | none | |
| An unimplemented public function is deleted, or is `[[noreturn]]` and throws `logic_error("not implemented: <name>")`, and gets no FFI binding | none | |
| Two functions sharing more than half their bodies merge behind a params struct; the test is whether a future change would land in both | none | |
| Trivially obvious literals need no name: `0`, `1`, `0.5` for a midpoint, array indices | extends [Avoid "magic constants"; use symbolic constants](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-magic) (ES.45) | |

## FFI conventions

The Core Guidelines have no FFI section. All eight are new.

| Candidate | CG | Policy |
|-----------|----|--------|
| Names cross the language boundary unchanged; no case conversion, no `_impl` shim | none | |
| The calling side validates before crossing; the callee may assert cheaply and does not re-validate | none | |
| Errors translate exactly once, at the binding layer, preserving type and message | none | |
| Absence maps to absence; NaN never crosses; an empty collection does not signal failure | none | |
| Unit conversion happens at the outer boundary, never at the FFI seam | none | |
| Ownership is explicit across the boundary: by-value copies, by-reference is non-owning with a documented lifetime, no raw pointers handed to the host | none | |
| A structure shared across the boundary has one schema and one source of truth; a schema change is versioned and moves both sides and the goldens together | none | |
| The binding layer is a declared escape hatch and is the one place boundary ceremony is correct | none | |

## Dependency direction

| Candidate | CG | Policy |
|-----------|----|--------|
| Layers run Input/CLI → Parser → IR/Model → Validation → Backend/Output, and includes flow rightward only | none | |
| A lower layer needing a higher layer's type gets an adapter at the boundary, not the higher layer's headers | none | |
| A wrapper type lives at the layer that owns its precondition, not the layer that consumes the value | none | |
| The inversion check: delete the higher-level module mentally; if the lower ones stop compiling, the dependency is inverted | none | |

## Real-time loops

| Candidate | CG | Policy |
|-----------|----|--------|
| Real-time loops pre-allocate; `push_back`, reallocating string operations, and anything reaching `malloc` are defects unless proven otherwise | none | |
| Real-time errors are recorded in a pre-allocated trace and surfaced at the scan boundary, never thrown | none | |
| A real-time loop does not call a runtime logger; it writes the trace structure | none | |
| A real-time loop has no unbounded loop, no unbounded lock acquisition, and no I/O | none | |

## Coroutines

[Do not use capturing lambdas that are coroutines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcoro-capture) (CP.51) and
[Parameters to coroutines should not be passed by reference](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcoro-reference-parameters) (CP.53)
already cover lambda captures and by-reference parameters. These two are not in the CG.

| Candidate | CG | Policy |
|-----------|----|--------|
| Awaitables are non-owning by default; an awaitable outliving the awaiting frame is an explicit ownership decision | none | |
| `co_await` chains deeper than two or three use symmetric transfer to bound stack growth | none | |

## Testing

The Core Guidelines have no testing section. All eight are new.

| Candidate | CG | Policy |
|-----------|----|--------|
| Test where the logic lives; pipeline tests are integration tests and there are few | none | |
| Do not test the language or the standard library | none | |
| Test the invariant, not the accessor | none | |
| Round-trip tests assert semantic equivalence, not textual identity | none | |
| One assertion of a behaviour; check what exists before adding a test file | none | |
| Use the project's test framework; no hand-rolled runners, no PASS/FAIL prints | none | |
| Structured output is golden-tested; every change is either no diff or a deliberate regeneration explained in the commit message | none | |
| A suite that would pass on a plausible wrong implementation is not testing | none | |

## Logging

The Core Guidelines have no logging section. All three are new.

| Candidate | CG | Policy |
|-----------|----|--------|
| No `std::cout` or `printf` in library code; they belong in CLI entry points | none | |
| Diagnostics go through a structured logger | none | |
| Log levels have fixed meanings: TRACE/DEBUG internal state, INFO operator-facing progress, WARN unexpected but recoverable, ERROR failed and continuing, FATAL cannot continue | none | |

## Naming

| Candidate | CG | Policy |
|-----------|----|--------|
| The case table is mandated machine-wide, not offered as a preference: `snake_case` functions and variables, trailing-underscore private members, `PascalCase` types and enumerators, `kPascalCase` constants, project-prefixed `ALL_CAPS` macros, `snake_case` namespaces and files | diverges [Prefer `underscore_style` names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-camel) (NL.10) | |
| Operation verbs are a fixed vocabulary shared with the Python convention: `parse_`, `format_`, `resolve_`, `*_to_*`, `validate_`, `build_`, `load_`, `write_`, `render_`, `expand_`, `plan_` | none | |
| A name prefix states the return contract: `is_`/`has_` returns `bool`, `try_` returns optional or result and never throws, `get_` cannot fail, `find_` returns optional or iterator, `make_` constructs | none | |

## Tooling commitments

The Core Guidelines have no tooling section. All six are new.

| Candidate | CG | Policy |
|-----------|----|--------|
| Warnings are `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror`, and any per-site disable carries a comment | none | |
| UBSan and ASan run in at least one configuration, TSan once concurrency exists; findings block merge | none | |
| clang-tidy runs `bugprone-*`, `cert-*`, `cppcoreguidelines-*`, `performance-*`, `readability-*`, with one comment per project-level disable | none | |
| Formatting is clang-format, decided once per project; baseline Google, indent 4, column limit 100 | none | |
| CMake by default; an alternative carries a stated reason | none | |
| The language standard is declared once in the top-level build config, and reaching past it is a bug | none | |

## Declared divergences

From the Divergences section. The GSL rows exist because the corpus takes no GSL dependency.

| Candidate | CG | Policy |
|-----------|----|--------|
| GSL is declined: structural preconditions become wrapper types, others are asserted, rather than `Expects()`/`Ensures()` | diverges [Prefer `Expects()` for expressing preconditions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-expects) (I.6), [Prefer `Ensures()` for expressing postconditions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-ensures) (I.8) | |
| `gsl::not_null` is declined; a never-null pointer is documented and asserted | diverges [Declare a pointer that must not be null as `not_null`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-nullptr) (I.12), [Use a `not_null<T>` to indicate that "null" is not a valid value](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-nullptr) (F.23) | |
| `gsl::index` is declined; subscript arithmetic uses a signed type | diverges [Don't use `unsigned` for subscripts, prefer `gsl::index`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-subscripts) (ES.107) | |
| The header extension is `.hpp`, not `.h`, to distinguish C++ from C headers in a mixed FFI tree | diverges [Use a `.cpp` suffix for code files and `.h` for interface files if your project doesn't already follow another convention](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-file-suffix) (SF.1) | |
| Concepts on every template argument is gated on C++20; earlier standards carry the same information in a `static_assert` | diverges [Specify concepts for all template arguments](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-concepts) (T.10) | |
