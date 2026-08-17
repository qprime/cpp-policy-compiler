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

58 rows carry a policy and 11 are struck to the coding standard. Of the 58, 21
policies were written from this list; the other 37 rows were already answered by
a policy derived from [CG-WORKLIST.md](CG-WORKLIST.md), because both lists
derive from the same conventions.md and a threshold or escape usually belongs in
the body of the policy it qualifies rather than in a policy of its own.

## Tier 1

| Candidate | CG | Policy |
|-----------|----|--------|
| Errors carry a four-part message: what failed, what field, what constraint, actual value | none | [POL-0228](POL-0228-four-part-error-message.md) |
| Dependency direction holds; includes flow one way through the layer stack | none | [POL-0218](POL-0218-dependencies-form-a-dag.md) |
| Determinism extends to output: no unordered-container iteration order, no platform-dependent floating point in golden output | extends [Ideally, a program should be statically type safe](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-typesafe) (P.4), [Always initialize an object](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-always) (ES.20) | [POL-0007](POL-0007-determinism-default.md) |

## Tier 3 escapes

| Candidate | CG | Policy |
|-----------|----|--------|
| Dimensioned scalars stay primitives with unit-suffixed names; a strong typedef requires two confusable units at a boundary *and* arithmetic that does not flow through the type | diverges [Make interfaces precisely and strongly typed](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-typed) (I.4) | [POL-0229](POL-0229-strong-typedef-threshold.md) |
| Exceptions are permitted at module boundaries, forbidden in real-time loops, never cross FFI un-translated; `-fno-exceptions` is per-module and declared in that module's top-level header | diverges [Throw an exception to signal that a function can't perform its assigned task](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-throw) (E.2), [Use exceptions to signal a failure to perform a required task](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-except) (I.10) | [POL-0184](POL-0184-exceptions-are-exceptional.md) |
| The FFI layer is a declared escape hatch from validate-at-the-boundary and is permitted the boilerplate that implies | extends [Catch run-time errors early](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-early) (P.7) | [POL-0230](POL-0230-binding-layer-is-a-declared-escape-hatch.md) |

## Patterns

| Candidate | CG | Policy |
|-----------|----|--------|
| A type with a validating constructor gets a static `try_from` that delegates to the constructor rather than duplicating the validation | none | [POL-0058](POL-0058-value-type-with-invariant.md) |
| More than four parameters triggers a params struct regardless of types; two adjacent same-type parameters trigger it regardless of count | extends [Keep the number of function arguments low](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-nargs) (I.23), [Avoid adjacent parameters that can be invoked by the same arguments in either order with different meaning](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-unrelated) (I.24) | [POL-0024](POL-0024-params-struct.md) |
| Ordered mathematical arguments are the named escape: `lerp(a, b, t)`, `clamp(v, lo, hi)`, `atan2(y, x)` | extends [Keep the number of function arguments low](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-nargs) (I.23) | [POL-0024](POL-0024-params-struct.md) |
| Naming the parameters and giving them distinct types are alternative ways to satisfy the adjacent-parameter rule; both are not required | extends [Avoid adjacent parameters that can be invoked by the same arguments in either order with different meaning](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-unrelated) (I.24) | [POL-0024](POL-0024-params-struct.md) |
| ~~Include guards are named `PROJECT_COMPONENT_FILE_HPP`; `#pragma once` is a vendor extension and is not used~~ | extends [Use `#include` guards for all header files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-guards) (SF.8) | coding standard — include guards |
| Scalar preconditions get no wrapper type; wrappers are for structural preconditions | none | [POL-0018](POL-0018-structural-precondition-wrapper.md) |
| Repeated asserts of the same precondition are a missing wrapper type | extends [State preconditions (if any)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-pre) (I.5) | [POL-0019](POL-0019-preconditions-asserted-not-gsl.md) |
| Silent partial output is never an acceptable failure mode | none | [POL-0183](POL-0183-failure-mechanism.md) |
| Failure becomes less fatal moving outward: FFI translates, module API returns a result, internals trust, the real-time loop records and continues, the loop boundary inspects the trace | none | [POL-0183](POL-0183-failure-mechanism.md) |

## Decision procedures

| Candidate | CG | Policy |
|-----------|----|--------|
| A thing becomes a type by an ordered test: invariant, then structural precondition, then fixed alternatives, then values travelling together, then confusable-without-arithmetic, else a primitive with a unit-suffixed name | none | [POL-0017](POL-0017-interface-takes-the-meaningful-type.md) |
| A strong typedef is not introduced where arithmetic flows through the value; a partial units type is ceremony without safety | diverges [Make interfaces precisely and strongly typed](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-typed) (I.4) | [POL-0229](POL-0229-strong-typedef-threshold.md) |
| Inheritance waits for the second concrete case; with one in hand, write the function | none | [POL-0065](POL-0065-concrete-types-over-hierarchies.md) |

## Traps

| Candidate | CG | Policy |
|-----------|----|--------|
| A variant visitor carries one overload per alternative and never a generic `[](auto&&)` fallback | none | [POL-0066](POL-0066-closed-set-variation.md) |
| A non-owning view is never stored as a member; it is an owning member or a call-duration parameter | none | [POL-0224](POL-0224-stored-view.md) |
| Every type is single-threaded by contract until a threading model is declared; a mutex member without one is removed | diverges [Assume that your code will run as part of a multi-threaded program](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-multi) (CP.1) | [POL-0163](POL-0163-single-threaded-by-contract.md) |
| `auto` is for a type obvious from the right-hand side or unspellable, not where the type is the load-bearing fact | diverges [Use `auto` to avoid redundant repetition of type names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-auto) (ES.11) | [POL-0123](POL-0123-auto-where-the-type-is-redundant.md) |
| `(void)param;` is allowed only where an override or interface mandates the signature; on a leaf function the parameter is deleted | none | [POL-0034](POL-0034-unused-parameter-unnamed.md) |
| An unimplemented public function is deleted, or is `[[noreturn]]` and throws `logic_error("not implemented: <name>")`, and gets no FFI binding | none | [POL-0231](POL-0231-unimplemented-function-is-absent-or-loud.md) |
| Two functions sharing more than half their bodies merge behind a params struct; the test is whether a future change would land in both | none | [POL-0118](POL-0118-one-definition-of-shared-logic.md) |
| Trivially obvious literals need no name: `0`, `1`, `0.5` for a midpoint, array indices | extends [Avoid "magic constants"; use symbolic constants](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-magic) (ES.45) | [POL-0133](POL-0133-named-constants.md) |

## FFI conventions

The Core Guidelines have no FFI section. All eight are new.

| Candidate | CG | Policy |
|-----------|----|--------|
| Names cross the language boundary unchanged; no case conversion, no `_impl` shim | none | [POL-0233](POL-0233-names-cross-unchanged.md) |
| The calling side validates before crossing; the callee may assert cheaply and does not re-validate | none | [POL-0234](POL-0234-caller-validates-before-crossing.md) |
| Errors translate exactly once, at the binding layer, preserving type and message | none | [POL-0187](POL-0187-translate-exceptions-once.md) |
| Absence maps to absence; NaN never crosses; an empty collection does not signal failure | none | [POL-0235](POL-0235-absence-maps-to-absence.md) |
| Unit conversion happens at the outer boundary, never at the FFI seam | none | [POL-0236](POL-0236-units-convert-at-the-outer-boundary.md) |
| Ownership is explicit across the boundary: by-value copies, by-reference is non-owning with a documented lifetime, no raw pointers handed to the host | none | [POL-0237](POL-0237-ffi-ownership-is-explicit.md) |
| A structure shared across the boundary has one schema and one source of truth; a schema change is versioned and moves both sides and the goldens together | none | [POL-0238](POL-0238-shared-schema-has-one-source-of-truth.md) |
| The binding layer is a declared escape hatch and is the one place boundary ceremony is correct | none | [POL-0230](POL-0230-binding-layer-is-a-declared-escape-hatch.md) |

## Dependency direction

| Candidate | CG | Policy |
|-----------|----|--------|
| Layers run Input/CLI → Parser → IR/Model → Validation → Backend/Output, and includes flow rightward only | none | [POL-0218](POL-0218-dependencies-form-a-dag.md) |
| A lower layer needing a higher layer's type gets an adapter at the boundary, not the higher layer's headers | none | [POL-0218](POL-0218-dependencies-form-a-dag.md) |
| A wrapper type lives at the layer that owns its precondition, not the layer that consumes the value | none | [POL-0239](POL-0239-wrapper-type-lives-at-its-layer.md) |
| The inversion check: delete the higher-level module mentally; if the lower ones stop compiling, the dependency is inverted | none | [POL-0218](POL-0218-dependencies-form-a-dag.md) |

## Real-time loops

| Candidate | CG | Policy |
|-----------|----|--------|
| Real-time loops pre-allocate; `push_back`, reallocating string operations, and anything reaching `malloc` are defects unless proven otherwise | none | [POL-0161](POL-0161-no-allocation-on-the-critical-path.md) |
| Real-time errors are recorded in a pre-allocated trace and surfaced at the scan boundary, never thrown | none | [POL-0162](POL-0162-no-context-switches-on-the-critical-path.md) |
| A real-time loop does not call a runtime logger; it writes the trace structure | none | [POL-0162](POL-0162-no-context-switches-on-the-critical-path.md) |
| A real-time loop has no unbounded loop, no unbounded lock acquisition, and no I/O | none | [POL-0162](POL-0162-no-context-switches-on-the-critical-path.md) |

## Coroutines

[Do not use capturing lambdas that are coroutines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcoro-capture) (CP.51) and
[Parameters to coroutines should not be passed by reference](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcoro-reference-parameters) (CP.53)
already cover lambda captures and by-reference parameters. These two are not in the CG.

| Candidate | CG | Policy |
|-----------|----|--------|
| Awaitables are non-owning by default; an awaitable outliving the awaiting frame is an explicit ownership decision | none | [POL-0182](POL-0182-bound-coroutine-chain-depth.md) |
| `co_await` chains deeper than two or three use symmetric transfer to bound stack growth | none | [POL-0182](POL-0182-bound-coroutine-chain-depth.md) |

## Testing

The Core Guidelines have no testing section. All eight are new.

| Candidate | CG | Policy |
|-----------|----|--------|
| Test where the logic lives; pipeline tests are integration tests and there are few | none | [POL-0240](POL-0240-test-where-the-logic-lives.md) |
| Do not test the language or the standard library | none | [POL-0241](POL-0241-do-not-test-the-language.md) |
| Test the invariant, not the accessor | none | [POL-0242](POL-0242-test-the-invariant-not-the-accessor.md) |
| Round-trip tests assert semantic equivalence, not textual identity | none | [POL-0243](POL-0243-round-trip-asserts-semantic-equivalence.md) |
| One assertion of a behaviour; check what exists before adding a test file | none | [POL-0244](POL-0244-one-assertion-of-a-behaviour.md) |
| Use the project's test framework; no hand-rolled runners, no PASS/FAIL prints | none | [POL-0245](POL-0245-use-the-project-test-framework.md) |
| Structured output is golden-tested; every change is either no diff or a deliberate regeneration explained in the commit message | none | [POL-0246](POL-0246-golden-tested-structured-output.md) |
| A suite that would pass on a plausible wrong implementation is not testing | none | [POL-0247](POL-0247-include-a-test-that-would-fail.md) |

## Logging

The Core Guidelines have no logging section. All three are new.

| Candidate | CG | Policy |
|-----------|----|--------|
| No `std::cout` or `printf` in library code; they belong in CLI entry points | none | [POL-0225](POL-0225-no-stream-output-in-library-code.md) |
| Diagnostics go through a structured logger | none | [POL-0225](POL-0225-no-stream-output-in-library-code.md) |
| Log levels have fixed meanings: TRACE/DEBUG internal state, INFO operator-facing progress, WARN unexpected but recoverable, ERROR failed and continuing, FATAL cannot continue | none | [POL-0248](POL-0248-log-levels-have-fixed-meanings.md) |

## Naming

| Candidate | CG | Policy |
|-----------|----|--------|
| ~~The case table is mandated machine-wide, not offered as a preference: `snake_case` functions and variables, trailing-underscore private members, `PascalCase` types and enumerators, `kPascalCase` constants, project-prefixed `ALL_CAPS` macros, `snake_case` namespaces and files~~ | diverges [Prefer `underscore_style` names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-camel) (NL.10) | coding standard — case table |
| ~~Operation verbs are a fixed vocabulary shared with the Python convention: `parse_`, `format_`, `resolve_`, `*_to_*`, `validate_`, `build_`, `load_`, `write_`, `render_`, `expand_`, `plan_`~~ | none | coding standard — operation verb vocabulary |
| ~~A name prefix states the return contract: `is_`/`has_` returns `bool`, `try_` returns optional or result and never throws, `get_` cannot fail, `find_` returns optional or iterator, `make_` constructs~~ | none | coding standard — return-contract prefixes |

## Tooling commitments

The Core Guidelines have no tooling section. All six are new.

| Candidate | CG | Policy |
|-----------|----|--------|
| ~~Warnings are `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror`, and any per-site disable carries a comment~~ | none | coding standard — warning set |
| ~~UBSan and ASan run in at least one configuration, TSan once concurrency exists; findings block merge~~ | none | coding standard — sanitizer configuration |
| ~~clang-tidy runs `bugprone-*`, `cert-*`, `cppcoreguidelines-*`, `performance-*`, `readability-*`, with one comment per project-level disable~~ | none | coding standard — static analysis check families |
| ~~Formatting is clang-format, decided once per project; baseline Google, indent 4, column limit 100~~ | none | coding standard — formatter configuration |
| ~~CMake by default; an alternative carries a stated reason~~ | none | coding standard — build system |
| ~~The language standard is declared once in the top-level build config, and reaching past it is a bug~~ | none | coding standard — language standard declaration |

## Declared divergences

From the Divergences section. The GSL rows exist because the corpus takes no GSL dependency.

| Candidate | CG | Policy |
|-----------|----|--------|
| GSL is declined: structural preconditions become wrapper types, others are asserted, rather than `Expects()`/`Ensures()` | diverges [Prefer `Expects()` for expressing preconditions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-expects) (I.6), [Prefer `Ensures()` for expressing postconditions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-ensures) (I.8) | [POL-0019](POL-0019-preconditions-asserted-not-gsl.md) |
| `gsl::not_null` is declined; a never-null pointer is documented and asserted | diverges [Declare a pointer that must not be null as `not_null`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-nullptr) (I.12), [Use a `not_null<T>` to indicate that "null" is not a valid value](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-nullptr) (F.23) | [POL-0022](POL-0022-non-null-pointer-documented.md) |
| `gsl::index` is declined; subscript arithmetic uses a signed type | diverges [Don't use `unsigned` for subscripts, prefer `gsl::index`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-subscripts) (ES.107) | [POL-0135](POL-0135-signed-arithmetic-unsigned-bits.md) |
| ~~The header extension is `.hpp`, not `.h`, to distinguish C++ from C headers in a mixed FFI tree~~ | diverges [Use a `.cpp` suffix for code files and `.h` for interface files if your project doesn't already follow another convention](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-file-suffix) (SF.1) | coding standard — file extensions |
| Concepts on every template argument is gated on C++20; earlier standards carry the same information in a `static_assert` | diverges [Specify concepts for all template arguments](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-concepts) (T.10) | [POL-0199](POL-0199-constrain-every-template-parameter.md) |
