# Core Guidelines worklist

Temporary. One row per Core Guidelines rule, in document order. Fill the
**Policy** column with a link to the policy file as each is written; strike
rows that will not become policies.

Rule titles are quoted from the Core Guidelines, which are under an MIT-style
licence. Source: <https://github.com/isocpp/CppCoreGuidelines>

466 rules. FAQ, NR (non-rules and myths), and In.0 are excluded as
non-normative.

423 rows carry a policy; 226 policies cover them, because one decision often
answers several rules. 43 rows are struck: 40 belong to the coding standard
rather than the corpus — see [STANDARD-TOPICS.md](STANDARD-TOPICS.md) — and
three are not rules (T.46 was removed upstream; T.101 and CP.201 are
placeholders).

## Sections

- [Philosophy](#philosophy) — 13 rules
- [Interfaces](#interfaces) — 20 rules
- [Functions](#functions) — 40 rules
- [Classes and class hierarchies](#classes-and-class-hierarchies) — 100 rules
- [Enumerations](#enumerations) — 8 rules
- [Resource management](#resource-management) — 25 rules
- [Expressions and statements](#expressions-and-statements) — 65 rules
- [Performance](#performance) — 18 rules
- [Concurrency](#concurrency) — 33 rules
- [Error handling](#error-handling) — 22 rules
- [Constants and immutability](#constants-and-immutability) — 5 rules
- [Templates and generic programming](#templates-and-generic-programming) — 53 rules
- [C-style programming](#c-style-programming) — 3 rules
- [Source files](#source-files) — 16 rules
- [Standard library](#standard-library) — 4 rules
- [Standard library — containers](#standard-library-containers) — 4 rules
- [Standard library — strings](#standard-library-strings) — 8 rules
- [Standard library — iostream](#standard-library-iostream) — 5 rules
- [Standard library — C stdlib](#standard-library-c-stdlib) — 1 rule
- [Architectural ideas](#architectural-ideas) — 3 rules
- [Naming and layout](#naming-and-layout) — 20 rules

## Philosophy

| Rule | Title | Policy |
|------|-------|--------|
| [P.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-direct) | Express ideas directly in code | [POL-0006](POL-0006-express-intent.md) |
| [P.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-cplusplus) | Write in ISO Standard C++ | [POL-0009](POL-0009-iso-standard-cpp.md) |
| [P.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-what) | Express intent | [POL-0006](POL-0006-express-intent.md) |
| [P.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-typesafe) | Ideally, a program should be statically type safe | [POL-0001](POL-0001-correct-by-construction.md) |
| [P.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-compile-time) | Prefer compile-time checking to run-time checking | [POL-0008](POL-0008-compiler-is-your-ally.md) |
| [P.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-run-time) | What cannot be checked at compile time should be checkable at run time | [POL-0002](POL-0002-failure-modes-visible.md) |
| [P.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-early) | Catch run-time errors early | [POL-0005](POL-0005-defensive-at-boundaries.md) |
| [P.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-leak) | Don't leak any resources | [POL-0003](POL-0003-ownership-is-obvious.md) |
| [P.9](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-waste) | Don't waste time or space | [POL-0010](POL-0010-cost-of-what-you-write.md) |
| [P.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-mutable) | Prefer immutable data to mutable data | [POL-0126](POL-0126-immutability-by-default.md) |
| [P.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-library) | Encapsulate messy constructs, rather than spreading through the code | [POL-0011](POL-0011-encapsulate-messy-constructs.md) |
| [P.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-tools) | Use supporting tools as appropriate | [POL-0012](POL-0012-tools-are-due-diligence.md) |
| [P.13](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rp-lib) | Use support libraries as appropriate | [POL-0013](POL-0013-standard-library-first.md) |

## Interfaces

| Rule | Title | Policy |
|------|-------|--------|
| [I.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-explicit) | Make interfaces explicit | [POL-0014](POL-0014-interface-states-its-dependencies.md) |
| [I.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-global) | Avoid non-`const` global variables | [POL-0015](POL-0015-no-mutable-globals.md) |
| [I.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-singleton) | Avoid singletons | [POL-0016](POL-0016-single-instance-is-passed-in.md) |
| [I.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-typed) | Make interfaces precisely and strongly typed | [POL-0017](POL-0017-interface-takes-the-meaningful-type.md) |
| [I.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-pre) | State preconditions (if any) | [POL-0018](POL-0018-structural-precondition-wrapper.md) |
| [I.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-expects) | Prefer `Expects()` for expressing preconditions | [POL-0019](POL-0019-preconditions-asserted-not-gsl.md) |
| [I.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-post) | State postconditions | [POL-0020](POL-0020-postcondition-in-return-type.md) |
| [I.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-ensures) | Prefer `Ensures()` for expressing postconditions | [POL-0019](POL-0019-preconditions-asserted-not-gsl.md) |
| [I.9](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-concepts) | If an interface is a template, document its parameters using concepts | [POL-0199](POL-0199-constrain-every-template-parameter.md) |
| [I.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-except) | Use exceptions to signal a failure to perform a required task | [POL-0184](POL-0184-exceptions-are-exceptional.md) |
| [I.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-raw) | Never transfer ownership by a raw pointer (`T*`) or reference (`T&`) | [POL-0021](POL-0021-no-ownership-through-raw-pointer.md) |
| [I.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-nullptr) | Declare a pointer that must not be null as `not_null` | [POL-0022](POL-0022-non-null-pointer-documented.md) |
| [I.13](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-array) | Do not pass an array as a single pointer | [POL-0042](POL-0042-pointer-and-length-pair.md) |
| [I.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-global-init) | Avoid complex initialization of global objects | [POL-0023](POL-0023-global-init-is-trivial.md) |
| [I.23](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-nargs) | Keep the number of function arguments low | [POL-0024](POL-0024-params-struct.md) |
| [I.24](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-unrelated) | Avoid adjacent parameters that can be invoked by the same arguments in either order with different meaning | [POL-0024](POL-0024-params-struct.md) |
| [I.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-abstract) | Prefer empty abstract classes as interfaces to class hierarchies | [POL-0025](POL-0025-interface-base-has-no-data.md) |
| [I.26](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-abi) | If you want a cross-compiler ABI, use a C-style subset | [POL-0026](POL-0026-abi-boundary-is-c-shaped.md) |
| [I.27](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-pimpl) | For stable library ABI, consider the Pimpl idiom | [POL-0027](POL-0027-pimpl-for-stable-abi.md) |
| [I.30](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-encapsulate) | Encapsulate rule violations | [POL-0028](POL-0028-encapsulate-rule-violations.md) |

## Functions

| Rule | Title | Policy |
|------|-------|--------|
| [F.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-package) | "Package" meaningful operations as carefully named functions | [POL-0029](POL-0029-named-operation.md) |
| [F.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-logical) | A function should perform a single logical operation | [POL-0029](POL-0029-named-operation.md) |
| [F.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-single) | Keep functions short and simple | [POL-0029](POL-0029-named-operation.md) |
| [F.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-constexpr) | If a function might have to be evaluated at compile time, declare it `constexpr` | [POL-0030](POL-0030-constexpr-what-you-can.md) |
| [F.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-inline) | If a function is very small and time-critical, declare it `inline` | [POL-0031](POL-0031-inline-only-when-measured.md) |
| [F.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-noexcept) | If your function must not throw, declare it `noexcept` | [POL-0032](POL-0032-noexcept-is-a-claim.md) |
| [F.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-smart) | For general use, take `T*` or `T&` arguments rather than smart pointers | [POL-0045](POL-0045-smart-pointer-parameter-says-lifetime.md) |
| [F.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-pure) | Prefer pure functions | [POL-0033](POL-0033-prefer-pure-functions.md) |
| [F.9](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-unused) | Unused parameters should be unnamed | [POL-0034](POL-0034-unused-parameter-unnamed.md) |
| [F.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-name) | If an operation can be reused, give it a name | [POL-0029](POL-0029-named-operation.md) |
| [F.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-lambda) | Use an unnamed lambda if you need a simple function object in one place only | [POL-0035](POL-0035-lambda-only-for-glue.md) |
| [F.15](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-conventional) | Prefer simple and conventional ways of passing information | [POL-0036](POL-0036-conventional-parameter-passing.md) |
| [F.16](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-in) | For "in" parameters, pass cheaply-copied types by value and others by reference to `const` | [POL-0036](POL-0036-conventional-parameter-passing.md) |
| [F.17](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-inout) | For "in-out" parameters, pass by reference to non-`const` | [POL-0036](POL-0036-conventional-parameter-passing.md) |
| [F.18](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-consume) | For "will-move-from" parameters, pass by `X&&` and `std::move` the parameter | [POL-0038](POL-0038-move-from-parameter.md) |
| [F.19](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-forward) | For "forward" parameters, pass by `TP&&` and only `std::forward` the parameter | [POL-0039](POL-0039-forwarding-parameter.md) |
| [F.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out) | For "out" output values, prefer return values to output parameters | [POL-0037](POL-0037-output-is-returned.md) |
| [F.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out-multi) | To return multiple "out" values, prefer returning a struct | [POL-0037](POL-0037-output-is-returned.md) |
| [F.60](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-ptr-ref) | Prefer `T*` over `T&` when "no argument" is a valid option | [POL-0036](POL-0036-conventional-parameter-passing.md) |
| [F.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-ptr) | Use `T*` or `owner<T*>` to designate a single object | [POL-0040](POL-0040-raw-pointer-one-object-non-owning.md) |
| [F.23](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-nullptr) | Use a `not_null<T>` to indicate that "null" is not a valid value | [POL-0022](POL-0022-non-null-pointer-documented.md) |
| [F.24](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-range) | Use a `span<T>` or a `span_p<T>` to designate a half-open sequence | [POL-0041](POL-0041-sequence-parameter-carries-bounds.md) |
| [F.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-zstring) | Use a `zstring` or a `not_null<zstring>` to designate a C-style string | [POL-0043](POL-0043-c-string-converted-on-entry.md) |
| [F.26](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-unique_ptr) | Use a `unique_ptr<T>` to transfer ownership where a pointer is needed | [POL-0044](POL-0044-ownership-decision.md) |
| [F.27](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-shared_ptr) | Use a `shared_ptr<T>` to share ownership | [POL-0044](POL-0044-ownership-decision.md) |
| [F.42](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-ptr) | Return a `T*` to indicate a position (only) | [POL-0046](POL-0046-return-pointer-means-position.md) |
| [F.43](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-dangle) | Never (directly or indirectly) return a pointer or a reference to a local object | [POL-0047](POL-0047-never-return-dangling.md) |
| [F.44](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-ref) | Return a `T&` when copy is undesirable and "returning no object" isn't needed | [POL-0048](POL-0048-return-reference-when-copy-costs.md) |
| [F.45](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-ref-ref) | Don't return a `T&&` | [POL-0049](POL-0049-no-rvalue-reference-return.md) |
| [F.46](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-main) | `int` is the return type for `main()` | [POL-0050](POL-0050-main-returns-int.md) |
| [F.47](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-assignment-op) | Return `T&` from assignment operators | [POL-0078](POL-0078-assignment-operator-shape.md) |
| [F.48](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-move-local) | Don't `return std::move(local)` | [POL-0049](POL-0049-no-rvalue-reference-return.md) |
| [F.49](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-const) | Don't return `const T` | [POL-0051](POL-0051-no-const-value-return.md) |
| [F.50](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-capture-vs-overload) | Use a lambda when a function won't do (to capture local variables, or to write a local function) | [POL-0035](POL-0035-lambda-only-for-glue.md) |
| [F.51](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-default-args) | Where there is a choice, prefer default arguments over overloading | [POL-0052](POL-0052-default-arguments-over-overloads.md) |
| [F.52](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-reference-capture) | Prefer capturing by reference in lambdas that will be used locally, including passed to algorithms | [POL-0054](POL-0054-escaping-lambda-captures-by-value.md) |
| [F.53](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-value-capture) | Avoid capturing by reference in lambdas that will be used non-locally, including returned, stored on the heap, or passed to another thread | [POL-0054](POL-0054-escaping-lambda-captures-by-value.md) |
| [F.54](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-this-capture) | When writing a lambda that captures `this` or any class data member, don't use `[=]` default capture | [POL-0053](POL-0053-explicit-lambda-captures.md) |
| [F.55](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f-varargs) | Don't use `va_arg` arguments | [POL-0055](POL-0055-no-va-arg.md) |
| [F.56](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f-nesting) | Avoid unnecessary condition nesting | [POL-0056](POL-0056-early-return-over-nesting.md) |

## Classes and class hierarchies

| Rule | Title | Policy |
|------|-------|--------|
| [C.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-org) | Organize related data into structures (`struct`s or `class`es) | [POL-0057](POL-0057-group-related-data.md) |
| [C.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-struct) | Use `class` if the class has an invariant; use `struct` if the data members can vary independently | [POL-0058](POL-0058-value-type-with-invariant.md) |
| [C.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-interface) | Represent the distinction between an interface and an implementation using a class | [POL-0090](POL-0090-interface-base-is-pure-abstract.md) |
| [C.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-member) | Make a function a member only if it needs direct access to the representation of a class | [POL-0061](POL-0061-free-function-by-default.md) |
| [C.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-helper) | Place helper functions in the same namespace as the class they support | [POL-0061](POL-0061-free-function-by-default.md) |
| [C.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-standalone) | Don't define a class or enum and declare a variable of its type in the same statement | [POL-0062](POL-0062-one-declaration-per-statement.md) |
| [C.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-class) | Use `class` rather than `struct` if any member is non-public | [POL-0058](POL-0058-value-type-with-invariant.md) |
| [C.9](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-private) | Minimize exposure of members | [POL-0063](POL-0063-members-are-private.md) |
| [C.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-concrete) | Prefer concrete types over class hierarchies | [POL-0065](POL-0065-concrete-types-over-hierarchies.md) |
| [C.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-regular) | Make concrete types regular | [POL-0069](POL-0069-concrete-types-are-regular.md) |
| [C.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-constref) | Don't make data members `const` or references in a copyable or movable type | [POL-0070](POL-0070-no-const-or-reference-members.md) |
| [C.13](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-lifetime) | If data member `B` uses another data member `A`, declare `A` before `B` | [POL-0059](POL-0059-initialize-in-the-member-init-list.md) |
| [C.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-zero) | If you can avoid defining default operations, do | [POL-0071](POL-0071-rule-of-zero.md) |
| [C.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-five) | If you define or `=delete` any copy, move, or destructor function, define or `=delete` them all | [POL-0071](POL-0071-rule-of-zero.md) |
| [C.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-matched) | Make default operations consistent | [POL-0071](POL-0071-rule-of-zero.md) |
| [C.30](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor) | Define a destructor if a class needs an explicit action at object destruction | [POL-0072](POL-0072-resource-owner-owns-only-that.md) |
| [C.31](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-release) | All resources acquired by a class must be released by the class's destructor | [POL-0072](POL-0072-resource-owner-owns-only-that.md) |
| [C.32](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-ptr) | If a class has a raw pointer (`T*`) or reference (`T&`), consider whether it might be owning | [POL-0072](POL-0072-resource-owner-owns-only-that.md) |
| [C.33](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-ptr2) | If a class has an owning pointer member, define a destructor | [POL-0072](POL-0072-resource-owner-owns-only-that.md) |
| [C.35](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-virtual) | A base class destructor should be either public and virtual, or protected and non-virtual | [POL-0073](POL-0073-base-destructor-public-virtual-or-protected.md) |
| [C.36](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-fail) | A destructor must not fail | [POL-0074](POL-0074-destructors-do-not-fail.md) |
| [C.37](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-noexcept) | Make destructors `noexcept` | [POL-0074](POL-0074-destructors-do-not-fail.md) |
| [C.40](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-ctor) | Define a constructor if a class has an invariant | [POL-0058](POL-0058-value-type-with-invariant.md) |
| [C.41](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-complete) | A constructor should create a fully initialized object | [POL-0058](POL-0058-value-type-with-invariant.md) |
| [C.42](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-throw) | If a constructor cannot construct a valid object, throw an exception | [POL-0058](POL-0058-value-type-with-invariant.md) |
| [C.43](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-default0) | Ensure that a copyable class has a default constructor | [POL-0075](POL-0075-default-constructor-is-cheap-or-absent.md) |
| [C.44](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-default00) | Prefer default constructors to be simple and non-throwing | [POL-0075](POL-0075-default-constructor-is-cheap-or-absent.md) |
| [C.45](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-default) | Don't define a default constructor that only initializes data members; use default member initializers instead | [POL-0059](POL-0059-initialize-in-the-member-init-list.md) |
| [C.46](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-explicit) | By default, declare single-argument constructors explicit | [POL-0060](POL-0060-explicit-single-argument-constructor.md) |
| [C.47](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-order) | Define and initialize data members in the order of member declaration | [POL-0059](POL-0059-initialize-in-the-member-init-list.md) |
| [C.48](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-in-class-initializer) | Prefer default member initializers to member initializers in constructors for constant initializers | [POL-0059](POL-0059-initialize-in-the-member-init-list.md) |
| [C.49](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-initialize) | Prefer initialization to assignment in constructors | [POL-0059](POL-0059-initialize-in-the-member-init-list.md) |
| [C.50](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-factory) | Use a factory function if you need "virtual behavior" during initialization | [POL-0076](POL-0076-factory-for-virtual-behaviour-at-construction.md) |
| [C.51](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-delegating) | Use delegating constructors to represent common actions for all constructors of a class | [POL-0077](POL-0077-delegating-and-inheriting-constructors.md) |
| [C.52](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-inheriting) | Use inheriting constructors to import constructors into a derived class that does not need further explicit initialization | [POL-0077](POL-0077-delegating-and-inheriting-constructors.md) |
| [C.60](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-copy-assignment) | Make copy assignment non-`virtual`, take the parameter by `const&`, and return by non-`const&` | [POL-0078](POL-0078-assignment-operator-shape.md) |
| [C.61](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-copy-semantic) | A copy operation should copy | [POL-0079](POL-0079-copy-copies-move-leaves-valid.md) |
| [C.62](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-copy-self) | Make copy assignment safe for self-assignment | [POL-0079](POL-0079-copy-copies-move-leaves-valid.md) |
| [C.63](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-move-assignment) | Make move assignment non-`virtual`, take the parameter by `&&`, and return by non-`const&` | [POL-0078](POL-0078-assignment-operator-shape.md) |
| [C.64](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-move-semantic) | A move operation should move and leave its source in a valid state | [POL-0079](POL-0079-copy-copies-move-leaves-valid.md) |
| [C.65](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-move-self) | Make move assignment safe for self-assignment | [POL-0079](POL-0079-copy-copies-move-leaves-valid.md) |
| [C.66](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-move-noexcept) | Make move operations `noexcept` | [POL-0080](POL-0080-move-operations-noexcept.md) |
| [C.67](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-copy-virtual) | A polymorphic class should suppress public copy/move | [POL-0081](POL-0081-polymorphic-types-suppress-copy.md) |
| [C.80](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-eqdefault) | Use `=default` if you have to be explicit about using the default semantics | [POL-0082](POL-0082-default-and-delete-are-explicit.md) |
| [C.81](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-delete) | Use `=delete` when you want to disable default behavior (without wanting an alternative) | [POL-0082](POL-0082-default-and-delete-are-explicit.md) |
| [C.82](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-ctor-virtual) | Don't call virtual functions in constructors and destructors | [POL-0083](POL-0083-no-virtual-calls-during-construction.md) |
| [C.83](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-swap) | For value-like types, consider providing a `noexcept` swap function | [POL-0084](POL-0084-swap-is-noexcept-and-cannot-fail.md) |
| [C.84](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-swap-fail) | A `swap` function must not fail | [POL-0084](POL-0084-swap-is-noexcept-and-cannot-fail.md) |
| [C.85](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-swap-noexcept) | Make `swap` `noexcept` | [POL-0084](POL-0084-swap-is-noexcept-and-cannot-fail.md) |
| [C.86](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-eq) | Make `==` symmetric with respect to operand types and `noexcept` | [POL-0085](POL-0085-equality-is-symmetric.md) |
| [C.87](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-eq-base) | Beware of `==` on base classes | [POL-0085](POL-0085-equality-is-symmetric.md) |
| [C.89](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-hash) | Make a `hash` `noexcept` | [POL-0086](POL-0086-hash-is-noexcept.md) |
| [C.90](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-memset) | Rely on constructors and assignment operators, not `memset` and `memcpy` | [POL-0087](POL-0087-no-memcpy-over-objects.md) |
| [C.100](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcon-stl) | Follow the STL when defining a container | [POL-0088](POL-0088-container-follows-the-standard-library.md) |
| [C.101](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcon-val) | Give a container value semantics | [POL-0088](POL-0088-container-follows-the-standard-library.md) |
| [C.102](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcon-move) | Give a container move operations | [POL-0088](POL-0088-container-follows-the-standard-library.md) |
| [C.103](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcon-init) | Give a container an initializer list constructor | [POL-0088](POL-0088-container-follows-the-standard-library.md) |
| [C.104](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcon-empty) | Give a container a default constructor that sets it to empty | [POL-0088](POL-0088-container-follows-the-standard-library.md) |
| [C.109](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcon-ptr) | If a resource handle has pointer semantics, provide `*` and `->` | [POL-0089](POL-0089-resource-handle-pointer-semantics.md) |
| [C.120](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-domain) | Use class hierarchies to represent concepts with inherent hierarchical structure (only) | [POL-0065](POL-0065-concrete-types-over-hierarchies.md) |
| [C.121](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-abstract) | If a base class is used as an interface, make it a pure abstract class | [POL-0090](POL-0090-interface-base-is-pure-abstract.md) |
| [C.122](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-separation) | Use abstract classes as interfaces when complete separation of interface and implementation is needed | [POL-0090](POL-0090-interface-base-is-pure-abstract.md) |
| [C.126](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-abstract-ctor) | An abstract class typically doesn't need a user-written constructor | [POL-0091](POL-0091-abstract-class-needs-no-constructor.md) |
| [C.127](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-dtor) | A class with a virtual function should have a virtual or protected destructor | [POL-0073](POL-0073-base-destructor-public-virtual-or-protected.md) |
| [C.128](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-override) | Virtual functions should specify exactly one of `virtual`, `override`, or `final` | [POL-0092](POL-0092-virtual-override-final-exactly-one.md) |
| [C.129](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-kind) | When designing a class hierarchy, distinguish between implementation inheritance and interface inheritance | [POL-0065](POL-0065-concrete-types-over-hierarchies.md) |
| [C.130](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-copy) | For making deep copies of polymorphic classes prefer a virtual `clone` function instead of public copy construction/assignment | [POL-0081](POL-0081-polymorphic-types-suppress-copy.md) |
| [C.131](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-get) | Avoid trivial getters and setters | [POL-0064](POL-0064-no-trivial-accessor-pairs.md) |
| [C.132](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-virtual) | Don't make a function `virtual` without reason | [POL-0065](POL-0065-concrete-types-over-hierarchies.md) |
| [C.133](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-protected) | Avoid `protected` data | [POL-0063](POL-0063-members-are-private.md) |
| [C.134](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-public) | Ensure all non-`const` data members have the same access level | [POL-0063](POL-0063-members-are-private.md) |
| [C.135](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-mi-interface) | Use multiple inheritance to represent multiple distinct interfaces | [POL-0093](POL-0093-multiple-inheritance-combines-interfaces.md) |
| [C.136](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-mi-implementation) | Use multiple inheritance to represent the union of implementation attributes | [POL-0093](POL-0093-multiple-inheritance-combines-interfaces.md) |
| [C.137](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-vbase) | Use `virtual` bases to avoid overly general base classes | [POL-0093](POL-0093-multiple-inheritance-combines-interfaces.md) |
| [C.138](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-using) | Create an overload set for a derived class and its bases with `using` | [POL-0094](POL-0094-using-declaration-restores-overload-set.md) |
| [C.139](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-final) | Use `final` on classes sparingly | [POL-0095](POL-0095-final-sparingly.md) |
| [C.140](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-virtual-default-arg) | Do not provide different default arguments for a virtual function and an overrider | [POL-0096](POL-0096-no-differing-default-arguments-on-overrides.md) |
| [C.145](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-poly) | Access polymorphic objects through pointers and references | [POL-0097](POL-0097-polymorphic-objects-by-handle.md) |
| [C.146](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-dynamic_cast) | Use `dynamic_cast` where class hierarchy navigation is unavoidable | [POL-0098](POL-0098-virtual-function-over-cast.md) |
| [C.147](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-ref-cast) | Use `dynamic_cast` to a reference type when failure to find the required class is considered an error | [POL-0098](POL-0098-virtual-function-over-cast.md) |
| [C.148](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-ptr-cast) | Use `dynamic_cast` to a pointer type when failure to find the required class is considered a valid alternative | [POL-0098](POL-0098-virtual-function-over-cast.md) |
| [C.149](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-smart) | Use `unique_ptr` or `shared_ptr` to avoid forgetting to `delete` objects created using `new` | [POL-0111](POL-0111-make-unique-and-make-shared.md) |
| [C.150](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-make_unique) | Use `make_unique()` to construct objects owned by `unique_ptr`s | [POL-0111](POL-0111-make-unique-and-make-shared.md) |
| [C.151](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-make_shared) | Use `make_shared()` to construct objects owned by `shared_ptr`s | [POL-0111](POL-0111-make-unique-and-make-shared.md) |
| [C.152](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-array) | Never assign a pointer to an array of derived class objects to a pointer to its base | [POL-0097](POL-0097-polymorphic-objects-by-handle.md) |
| [C.153](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-use-virtual) | Prefer virtual function to casting | [POL-0098](POL-0098-virtual-function-over-cast.md) |
| [C.160](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-conventional) | Define operators primarily to mimic conventional usage | [POL-0099](POL-0099-operators-keep-their-meaning.md) |
| [C.161](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-symmetric) | Use non-member functions for symmetric operators | [POL-0100](POL-0100-symmetric-operators-are-non-member.md) |
| [C.162](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-equivalent) | Overload operations that are roughly equivalent | [POL-0099](POL-0099-operators-keep-their-meaning.md) |
| [C.163](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-equivalent-2) | Overload only for operations that are roughly equivalent | [POL-0099](POL-0099-operators-keep-their-meaning.md) |
| [C.164](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-conversion) | Avoid implicit conversion operators | [POL-0101](POL-0101-no-implicit-conversion-operators.md) |
| [C.165](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-custom) | Use `using` for customization points | [POL-0102](POL-0102-customization-point-is-an-unqualified-call.md) |
| [C.166](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-address-of) | Overload unary `&` only as part of a system of smart pointers and references | [POL-0101](POL-0101-no-implicit-conversion-operators.md) |
| [C.167](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-overload) | Use an operator for an operation with its conventional meaning | [POL-0099](POL-0099-operators-keep-their-meaning.md) |
| [C.168](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-namespace) | Define overloaded operators in the namespace of their operands | [POL-0100](POL-0100-symmetric-operators-are-non-member.md) |
| [C.170](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ro-lambda) | If you feel like overloading a lambda, use a generic lambda | [POL-0103](POL-0103-generic-lambda-instead-of-overload-set.md) |
| [C.180](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ru-union) | Use `union`s to save memory | [POL-0066](POL-0066-closed-set-variation.md) |
| [C.181](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ru-naked) | Avoid "naked" `union`s | [POL-0066](POL-0066-closed-set-variation.md) |
| [C.182](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ru-anonymous) | Use anonymous `union`s to implement tagged unions | [POL-0066](POL-0066-closed-set-variation.md) |
| [C.183](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ru-pun) | Don't use a `union` for type punning | [POL-0227](POL-0227-no-type-punning.md) |

## Enumerations

| Rule | Title | Policy |
|------|-------|--------|
| [Enum.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#renum-macro) | Prefer enumerations over macros | [POL-0104](POL-0104-no-macros.md) |
| [Enum.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#renum-set) | Use enumerations to represent sets of related named constants | [POL-0105](POL-0105-enum-class-always.md) |
| [Enum.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#renum-class) | Prefer class enums over "plain" enums | [POL-0105](POL-0105-enum-class-always.md) |
| [Enum.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#renum-oper) | Define operations on enumerations for safe and simple use | [POL-0106](POL-0106-enum-operations-are-named-functions.md) |
| ~~[Enum.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#renum-caps)~~ | ~~Don't use `ALL_CAPS` for enumerators~~ | coding standard — case table |
| [Enum.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#renum-unnamed) | Avoid unnamed enumerations | [POL-0107](POL-0107-no-unnamed-enumerations.md) |
| [Enum.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#renum-underlying) | Specify the underlying type of an enumeration only when necessary | [POL-0108](POL-0108-enum-values-only-when-they-matter.md) |
| [Enum.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#renum-value) | Specify enumerator values only when necessary | [POL-0108](POL-0108-enum-values-only-when-they-matter.md) |

## Resource management

| Rule | Title | Policy |
|------|-------|--------|
| [R.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-raii) | Manage resources automatically using resource handles and RAII (Resource Acquisition Is Initialization) | [POL-0109](POL-0109-raii.md) |
| [R.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-use-ptr) | In interfaces, use raw pointers to denote individual objects (only) | [POL-0040](POL-0040-raw-pointer-one-object-non-owning.md) |
| [R.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ptr) | A raw pointer (a `T*`) is non-owning | [POL-0040](POL-0040-raw-pointer-one-object-non-owning.md) |
| [R.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ref) | A raw reference (a `T&`) is non-owning | [POL-0040](POL-0040-raw-pointer-one-object-non-owning.md) |
| [R.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-scoped) | Prefer scoped objects, don't heap-allocate unnecessarily | [POL-0044](POL-0044-ownership-decision.md) |
| [R.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-global) | Avoid non-`const` global variables | [POL-0015](POL-0015-no-mutable-globals.md) |
| [R.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-mallocfree) | Avoid `malloc()` and `free()` | [POL-0110](POL-0110-no-explicit-new-or-malloc.md) |
| [R.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete) | Avoid calling `new` and `delete` explicitly | [POL-0110](POL-0110-no-explicit-new-or-malloc.md) |
| [R.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-immediate-alloc) | Immediately give the result of an explicit resource allocation to a manager object | [POL-0111](POL-0111-make-unique-and-make-shared.md) |
| [R.13](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-single-alloc) | Perform at most one explicit resource allocation in a single expression statement | [POL-0111](POL-0111-make-unique-and-make-shared.md) |
| [R.14](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ap) | Avoid `[]` parameters, prefer `span` | [POL-0041](POL-0041-sequence-parameter-carries-bounds.md) |
| [R.15](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-pair) | Always overload matched allocation/deallocation pairs | [POL-0112](POL-0112-matched-allocation-pairs.md) |
| [R.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-owner) | Use `unique_ptr` or `shared_ptr` to represent ownership | [POL-0044](POL-0044-ownership-decision.md) |
| [R.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique) | Prefer `unique_ptr` over `shared_ptr` unless you need to share ownership | [POL-0044](POL-0044-ownership-decision.md) |
| [R.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_shared) | Use `make_shared()` to make `shared_ptr`s | [POL-0111](POL-0111-make-unique-and-make-shared.md) |
| [R.23](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_unique) | Use `make_unique()` to make `unique_ptr`s | [POL-0111](POL-0111-make-unique-and-make-shared.md) |
| [R.24](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-weak_ptr) | Use `std::weak_ptr` to break cycles of `shared_ptr`s | [POL-0113](POL-0113-weak-ptr-breaks-cycles.md) |
| [R.30](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrparam) | Take smart pointers as parameters only to explicitly express lifetime semantics | [POL-0045](POL-0045-smart-pointer-parameter-says-lifetime.md) |
| [R.31](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smart) | If you have non-`std` smart pointers, follow the basic pattern from `std` | [POL-0114](POL-0114-custom-smart-pointer-follows-std.md) |
| [R.32](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-uniqueptrparam) | Take a `unique_ptr<widget>` parameter to express that a function assumes ownership of a `widget` | [POL-0045](POL-0045-smart-pointer-parameter-says-lifetime.md) |
| [R.33](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-reseat) | Take a `unique_ptr<widget>&` parameter to express that a function reseats the `widget` | [POL-0045](POL-0045-smart-pointer-parameter-says-lifetime.md) |
| [R.34](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-owner) | Take a `shared_ptr<widget>` parameter to express shared ownership | [POL-0045](POL-0045-smart-pointer-parameter-says-lifetime.md) |
| [R.35](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam) | Take a `shared_ptr<widget>&` parameter to express that a function might reseat the shared pointer | [POL-0045](POL-0045-smart-pointer-parameter-says-lifetime.md) |
| [R.36](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-const) | Take a `const shared_ptr<widget>&` parameter to express that it might retain a reference count to the object ??? | [POL-0045](POL-0045-smart-pointer-parameter-says-lifetime.md) |
| [R.37](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrget) | Do not pass a pointer or reference obtained from an aliased smart pointer | [POL-0115](POL-0115-no-borrow-from-aliased-smart-pointer.md) |

## Expressions and statements

| Rule | Title | Policy |
|------|-------|--------|
| [ES.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-lib) | Prefer the standard library to other libraries and to "handcrafted code" | [POL-0013](POL-0013-standard-library-first.md) |
| [ES.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-abstr) | Prefer suitable abstractions to direct use of language features | [POL-0117](POL-0117-abstraction-over-language-feature.md) |
| [ES.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-dry) | Don't repeat yourself, avoid redundant code | [POL-0118](POL-0118-one-definition-of-shared-logic.md) |
| [ES.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-scope) | Keep scopes small | [POL-0120](POL-0120-name-introduced-where-valued.md) |
| [ES.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-cond) | Declare names in for-statement initializers and conditions to limit scope | [POL-0120](POL-0120-name-introduced-where-valued.md) |
| ~~[ES.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-name-length)~~ | ~~Keep common and local names short, and keep uncommon and non-local names longer~~ | coding standard — name length against scope |
| [ES.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-name-similar) | Avoid similar-looking names | [POL-0122](POL-0122-no-similar-looking-names.md) |
| ~~[ES.9](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-not-caps)~~ | ~~Avoid `ALL_CAPS` names~~ | coding standard — case table |
| ~~[ES.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-name-one)~~ | ~~Declare one name (only) per declaration~~ | coding standard — one thing per line |
| [ES.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-auto) | Use `auto` to avoid redundant repetition of type names | [POL-0123](POL-0123-auto-where-the-type-is-redundant.md) |
| [ES.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-reuse) | Do not reuse names in nested scopes | [POL-0121](POL-0121-one-variable-one-purpose.md) |
| [ES.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-always) | Always initialize an object | [POL-0125](POL-0125-everything-is-initialized.md) |
| [ES.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-introduce) | Don't introduce a variable (or constant) before you need to use it | [POL-0120](POL-0120-name-introduced-where-valued.md) |
| [ES.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-init) | Don't declare a variable until you have a value to initialize it with | [POL-0120](POL-0120-name-introduced-where-valued.md) |
| [ES.23](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-list) | Prefer the `{}`-initializer syntax | [POL-0125](POL-0125-everything-is-initialized.md) |
| [ES.24](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-unique) | Use a `unique_ptr<T>` to hold pointers | [POL-0044](POL-0044-ownership-decision.md) |
| [ES.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-const) | Declare an object `const` or `constexpr` unless you want to modify its value later on | [POL-0126](POL-0126-immutability-by-default.md) |
| [ES.26](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-recycle) | Don't use a variable for two unrelated purposes | [POL-0121](POL-0121-one-variable-one-purpose.md) |
| [ES.27](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-stack) | Use `std::array` or `stack_array` for arrays on the stack | [POL-0128](POL-0128-fixed-size-local-sequence.md) |
| [ES.28](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-lambda-init) | Use lambdas for complex initialization, especially of `const` variables | [POL-0129](POL-0129-lambda-for-complex-const-init.md) |
| [ES.30](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-macros) | Don't use macros for program text manipulation | [POL-0104](POL-0104-no-macros.md) |
| [ES.31](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-macros2) | Don't use macros for constants or "functions" | [POL-0104](POL-0104-no-macros.md) |
| ~~[ES.32](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-all_caps)~~ | ~~Use `ALL_CAPS` for all macro names~~ | coding standard — case table |
| ~~[ES.33](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-macros3)~~ | ~~If you must use macros, give them unique names~~ | coding standard — case table |
| [ES.40](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-complicated) | Avoid complicated expressions | [POL-0130](POL-0130-simple-expressions.md) |
| [ES.41](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-parens) | If in doubt about operator precedence, parenthesize | [POL-0130](POL-0130-simple-expressions.md) |
| [ES.42](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-ptr) | Keep use of pointers simple and straightforward | [POL-0131](POL-0131-simple-pointer-use.md) |
| [ES.43](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-order) | Avoid expressions with undefined order of evaluation | [POL-0132](POL-0132-no-evaluation-order-dependence.md) |
| [ES.44](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-order-fct) | Don't depend on order of evaluation of function arguments | [POL-0132](POL-0132-no-evaluation-order-dependence.md) |
| [ES.45](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-magic) | Avoid "magic constants"; use symbolic constants | [POL-0133](POL-0133-named-constants.md) |
| [ES.46](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-narrowing) | Avoid lossy (narrowing, truncating) arithmetic conversions | [POL-0136](POL-0136-no-narrowing-conversions.md) |
| [ES.47](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-nullptr) | Use `nullptr` rather than `0` or `NULL` | [POL-0137](POL-0137-nullptr-not-zero.md) |
| [ES.48](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-casts) | Avoid casts | [POL-0138](POL-0138-casts-are-named-and-rare.md) |
| [ES.49](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-casts-named) | If you must use a cast, use a named cast | [POL-0138](POL-0138-casts-are-named-and-rare.md) |
| [ES.50](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-casts-const) | Don't cast away `const` | [POL-0138](POL-0138-casts-are-named-and-rare.md) |
| [ES.55](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-range-checking) | Avoid the need for range checking | [POL-0139](POL-0139-no-range-checks-at-use.md) |
| [ES.56](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-move) | Write `std::move()` only when you need to explicitly move an object to another scope | [POL-0140](POL-0140-move-only-when-moving-out.md) |
| [ES.60](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-new) | Avoid `new` and `delete` outside resource management functions | [POL-0110](POL-0110-no-explicit-new-or-malloc.md) |
| [ES.61](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-del) | Delete arrays using `delete[]` and non-arrays using `delete` | [POL-0110](POL-0110-no-explicit-new-or-malloc.md) |
| [ES.62](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-arr2) | Don't compare pointers into different arrays | [POL-0141](POL-0141-no-cross-object-pointer-comparison.md) |
| [ES.63](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-slice) | Don't slice | [POL-0097](POL-0097-polymorphic-objects-by-handle.md) |
| [ES.64](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-construct) | Use the `T{e}`notation for construction | [POL-0125](POL-0125-everything-is-initialized.md) |
| [ES.65](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-deref) | Don't dereference an invalid pointer | [POL-0142](POL-0142-no-invalid-dereference.md) |
| [ES.70](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-switch-if) | Prefer a `switch`-statement to an `if`-statement when there is a choice | [POL-0143](POL-0143-switch-over-if-chain.md) |
| [ES.71](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-for-range) | Prefer a range-`for`-statement to a `for`-statement when there is a choice | [POL-0146](POL-0146-range-for-preferred.md) |
| [ES.72](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-for-while) | Prefer a `for`-statement to a `while`-statement when there is an obvious loop variable | [POL-0147](POL-0147-for-when-there-is-a-loop-variable.md) |
| [ES.73](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-while-for) | Prefer a `while`-statement to a `for`-statement when there is no obvious loop variable | [POL-0147](POL-0147-for-when-there-is-a-loop-variable.md) |
| [ES.74](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-for-init) | Prefer to declare a loop variable in the initializer part of a `for`-statement | [POL-0148](POL-0148-loop-variable-scope-and-stability.md) |
| [ES.75](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-do) | Avoid `do`-statements | [POL-0149](POL-0149-no-do-statement.md) |
| [ES.76](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-goto) | Avoid `goto` | [POL-0150](POL-0150-no-goto.md) |
| [ES.77](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-continue) | Minimize the use of `break` and `continue` in loops | [POL-0151](POL-0151-minimize-break-and-continue.md) |
| [ES.78](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-break) | Don't rely on implicit fallthrough in `switch` statements | [POL-0144](POL-0144-no-implicit-fallthrough.md) |
| [ES.79](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-default) | Use `default` to handle common cases (only) | [POL-0145](POL-0145-default-arm-is-for-common-cases.md) |
| [ES.84](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-noname) | Don't try to declare a local variable with no name | [POL-0152](POL-0152-no-unnamed-local.md) |
| [ES.85](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-empty) | Make empty statements visible | [POL-0153](POL-0153-visible-empty-statement.md) |
| [ES.86](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-loop-counter) | Avoid modifying loop control variables inside the body of raw for-loops | [POL-0148](POL-0148-loop-variable-scope-and-stability.md) |
| [ES.87](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-if) | Don't add redundant `==` or `!=` to conditions | [POL-0154](POL-0154-no-redundant-boolean-comparison.md) |
| [ES.100](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-mix) | Don't mix signed and unsigned arithmetic | [POL-0135](POL-0135-signed-arithmetic-unsigned-bits.md) |
| [ES.101](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-unsigned) | Use unsigned types for bit manipulation | [POL-0135](POL-0135-signed-arithmetic-unsigned-bits.md) |
| [ES.102](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-signed) | Use signed types for arithmetic | [POL-0135](POL-0135-signed-arithmetic-unsigned-bits.md) |
| [ES.103](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-overflow) | Don't overflow | [POL-0155](POL-0155-no-overflow-or-divide-by-zero.md) |
| [ES.104](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-underflow) | Don't underflow | [POL-0155](POL-0155-no-overflow-or-divide-by-zero.md) |
| [ES.105](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-zero) | Don't divide by integer zero | [POL-0155](POL-0155-no-overflow-or-divide-by-zero.md) |
| [ES.106](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-nonnegative) | Don't try to avoid negative values by using `unsigned` | [POL-0135](POL-0135-signed-arithmetic-unsigned-bits.md) |
| [ES.107](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-subscripts) | Don't use `unsigned` for subscripts, prefer `gsl::index` | [POL-0135](POL-0135-signed-arithmetic-unsigned-bits.md) |

## Performance

| Rule | Title | Policy |
|------|-------|--------|
| [Per.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-reason) | Don't optimize without reason | [POL-0156](POL-0156-optimize-what-measurement-named.md) |
| [Per.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-knuth) | Don't optimize prematurely | [POL-0156](POL-0156-optimize-what-measurement-named.md) |
| [Per.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-critical) | Don't optimize something that's not performance critical | [POL-0156](POL-0156-optimize-what-measurement-named.md) |
| [Per.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-simple) | Don't assume that complicated code is necessarily faster than simple code | [POL-0156](POL-0156-optimize-what-measurement-named.md) |
| [Per.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-low) | Don't assume that low-level code is necessarily faster than high-level code | [POL-0156](POL-0156-optimize-what-measurement-named.md) |
| [Per.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-measure) | Don't make claims about performance without measurements | [POL-0156](POL-0156-optimize-what-measurement-named.md) |
| [Per.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-efficiency) | Design to enable optimization | [POL-0157](POL-0157-design-to-enable-optimization.md) |
| [Per.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-type) | Rely on the static type system | [POL-0157](POL-0157-design-to-enable-optimization.md) |
| [Per.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-comp) | Move computation from run time to compile time | [POL-0030](POL-0030-constexpr-what-you-can.md) |
| [Per.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-alias) | Eliminate redundant aliases | [POL-0158](POL-0158-remove-redundant-indirection.md) |
| [Per.13](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-indirect) | Eliminate redundant indirections | [POL-0158](POL-0158-remove-redundant-indirection.md) |
| [Per.14](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-alloc) | Minimize the number of allocations and deallocations | [POL-0159](POL-0159-minimize-allocations.md) |
| [Per.15](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-alloc0) | Do not allocate on a critical branch | [POL-0161](POL-0161-no-allocation-on-the-critical-path.md) |
| [Per.16](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-compact) | Use compact data structures | [POL-0160](POL-0160-layout-follows-access.md) |
| [Per.17](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-struct) | Declare the most used member of a time-critical struct first | [POL-0160](POL-0160-layout-follows-access.md) |
| [Per.18](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-space) | Space is time | [POL-0160](POL-0160-layout-follows-access.md) |
| [Per.19](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-access) | Access memory predictably | [POL-0160](POL-0160-layout-follows-access.md) |
| [Per.30](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rper-context) | Avoid context switches on the critical path | [POL-0162](POL-0162-no-context-switches-on-the-critical-path.md) |

## Concurrency

| Rule | Title | Policy |
|------|-------|--------|
| [CP.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-multi) | Assume that your code will run as part of a multi-threaded program | [POL-0163](POL-0163-single-threaded-by-contract.md) |
| [CP.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-races) | Avoid data races | [POL-0165](POL-0165-no-data-races.md) |
| [CP.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-data) | Minimize explicit sharing of writable data | [POL-0165](POL-0165-no-data-races.md) |
| [CP.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-task) | Think in terms of tasks, rather than threads | [POL-0166](POL-0166-think-in-tasks.md) |
| [CP.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-volatile) | Don't try to use `volatile` for synchronization | [POL-0167](POL-0167-volatile-is-not-synchronization.md) |
| ~~[CP.9](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-tools)~~ | ~~Whenever feasible use tools to validate your concurrent code~~ | coding standard — sanitizer configuration |
| [CP.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-raii) | Use RAII, never plain `lock()`/`unlock()` | [POL-0169](POL-0169-locks-are-raii.md) |
| [CP.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-lock) | Use `std::lock()` or `std::scoped_lock` to acquire multiple `mutex`es | [POL-0170](POL-0170-acquire-multiple-locks-atomically.md) |
| [CP.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-unknown) | Never call unknown code while holding a lock (e.g., a callback) | [POL-0171](POL-0171-no-unknown-code-under-a-lock.md) |
| [CP.23](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-join) | Think of a joining `thread` as a scoped container | [POL-0172](POL-0172-threads-are-owned-and-joined.md) |
| [CP.24](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-detach) | Think of a `thread` as a global container | [POL-0172](POL-0172-threads-are-owned-and-joined.md) |
| [CP.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-joining_thread) | Prefer `gsl::joining_thread` over `std::thread` | [POL-0172](POL-0172-threads-are-owned-and-joined.md) |
| [CP.26](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-detached_thread) | Don't `detach()` a thread | [POL-0172](POL-0172-threads-are-owned-and-joined.md) |
| [CP.31](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-data-by-value) | Pass small amounts of data between threads by value, rather than by reference or pointer | [POL-0173](POL-0173-pass-data-between-threads-by-value.md) |
| [CP.32](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-shared) | To share ownership between unrelated `thread`s use `shared_ptr` | [POL-0173](POL-0173-pass-data-between-threads-by-value.md) |
| [CP.40](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-switch) | Minimize context switching | [POL-0162](POL-0162-no-context-switches-on-the-critical-path.md) |
| [CP.41](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-create) | Minimize thread creation and destruction | [POL-0162](POL-0162-no-context-switches-on-the-critical-path.md) |
| [CP.42](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-wait) | Don't `wait` without a condition | [POL-0174](POL-0174-wait-on-a-condition.md) |
| [CP.43](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-time) | Minimize time spent in a critical section | [POL-0175](POL-0175-short-critical-sections.md) |
| [CP.44](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-name) | Remember to name your `lock_guard`s and `unique_lock`s | [POL-0152](POL-0152-no-unnamed-local.md) |
| [CP.50](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-mutex) | Define a `mutex` together with the data it guards. Use `synchronized_value<T>` where possible | [POL-0176](POL-0176-mutex-lives-with-its-data.md) |
| [CP.51](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcoro-capture) | Do not use capturing lambdas that are coroutines | [POL-0180](POL-0180-coroutine-lambda-captures-by-value.md) |
| [CP.52](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcoro-locks) | Do not hold locks or other synchronization primitives across suspension points | [POL-0181](POL-0181-no-locks-across-suspension.md) |
| [CP.53](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcoro-reference-parameters) | Parameters to coroutines should not be passed by reference | [POL-0179](POL-0179-coroutine-parameters-by-value.md) |
| [CP.60](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-future) | Use a `future` to return a value from a concurrent task | [POL-0166](POL-0166-think-in-tasks.md) |
| [CP.61](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-async) | Use `async()` to spawn concurrent tasks | [POL-0166](POL-0166-think-in-tasks.md) |
| [CP.100](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-lockfree) | Don't use lock-free programming unless you absolutely have to | [POL-0177](POL-0177-lock-free-is-a-last-resort.md) |
| [CP.101](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-distrust) | Distrust your hardware/compiler combination | [POL-0177](POL-0177-lock-free-is-a-last-resort.md) |
| [CP.102](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-literature) | Carefully study the literature | [POL-0177](POL-0177-lock-free-is-a-last-resort.md) |
| [CP.110](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-double) | Do not write your own double-checked locking for initialization | [POL-0178](POL-0178-one-time-init-is-provided.md) |
| [CP.111](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-double-pattern) | Use a conventional pattern if you really need double-checked locking | [POL-0178](POL-0178-one-time-init-is-provided.md) |
| [CP.200](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-volatile2) | Use `volatile` only to talk to non-C++ memory | [POL-0167](POL-0167-volatile-is-not-synchronization.md) |
| ~~[CP.201](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconc-signal)~~ | ~~??? Signals~~ | placeholder, not a rule |

## Error handling

| Rule | Title | Policy |
|------|-------|--------|
| [E.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-design) | Develop an error-handling strategy early in a design | [POL-0183](POL-0183-failure-mechanism.md) |
| [E.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-throw) | Throw an exception to signal that a function can't perform its assigned task | [POL-0184](POL-0184-exceptions-are-exceptional.md) |
| [E.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-errors) | Use exceptions for error handling only | [POL-0184](POL-0184-exceptions-are-exceptional.md) |
| [E.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-design-invariants) | Design your error-handling strategy around invariants | [POL-0183](POL-0183-failure-mechanism.md) |
| [E.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-invariant) | Let a constructor establish an invariant, and throw if it cannot | [POL-0058](POL-0058-value-type-with-invariant.md) |
| [E.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-raii) | Use RAII to prevent leaks | [POL-0109](POL-0109-raii.md) |
| [E.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-precondition) | State your preconditions | [POL-0018](POL-0018-structural-precondition-wrapper.md) |
| [E.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-postcondition) | State your postconditions | [POL-0020](POL-0020-postcondition-in-return-type.md) |
| [E.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-noexcept) | Use `noexcept` when exiting a function because of a `throw` is impossible or unacceptable | [POL-0032](POL-0032-noexcept-is-a-claim.md) |
| [E.13](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-never-throw) | Never throw while being the direct owner of an object | [POL-0185](POL-0185-no-throw-while-owning.md) |
| [E.14](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-exception-types) | Use purpose-designed user-defined types as exceptions (not built-in types) | [POL-0186](POL-0186-exception-types-and-catching.md) |
| [E.15](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-exception-ref) | Throw by value, catch exceptions from a hierarchy by reference | [POL-0186](POL-0186-exception-types-and-catching.md) |
| [E.16](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-never-fail) | Destructors, deallocation, `swap`, and exception type copy/move construction must never fail | [POL-0074](POL-0074-destructors-do-not-fail.md) |
| [E.17](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-not-always) | Don't try to catch every exception in every function | [POL-0187](POL-0187-translate-exceptions-once.md) |
| [E.18](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-catch) | Minimize the use of explicit `try`/`catch` | [POL-0187](POL-0187-translate-exceptions-once.md) |
| [E.19](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-finally) | Use a `final_action` object to express cleanup if no suitable resource handle is available | [POL-0189](POL-0189-scope-guard-for-cleanup.md) |
| [E.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-no-throw-raii) | If you can't throw exceptions, simulate RAII for resource management | [POL-0190](POL-0190-exception-free-module-convention.md) |
| [E.26](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-no-throw-crash) | If you can't throw exceptions, consider failing fast | [POL-0190](POL-0190-exception-free-module-convention.md) |
| [E.27](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-no-throw-codes) | If you can't throw exceptions, use error codes systematically | [POL-0190](POL-0190-exception-free-module-convention.md) |
| [E.28](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-no-throw) | Avoid error handling based on global state (e.g. `errno`) | [POL-0191](POL-0191-no-error-state-in-globals.md) |
| [E.30](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-specifications) | Don't use exception specifications | [POL-0192](POL-0192-no-exception-specifications.md) |
| [E.31](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re_catch) | Properly order your `catch`-clauses | [POL-0186](POL-0186-exception-types-and-catching.md) |

## Constants and immutability

| Rule | Title | Policy |
|------|-------|--------|
| [Con.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconst-immutable) | By default, make objects immutable | [POL-0126](POL-0126-immutability-by-default.md) |
| [Con.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconst-fct) | By default, make member functions `const` | [POL-0127](POL-0127-const-on-what-does-not-mutate.md) |
| [Con.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconst-ref) | By default, pass pointers and references to `const`s | [POL-0127](POL-0127-const-on-what-does-not-mutate.md) |
| [Con.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconst-const) | Use `const` to define objects with values that do not change after construction | [POL-0126](POL-0126-immutability-by-default.md) |
| [Con.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconst-constexpr) | Use `constexpr` for values that can be computed at compile time | [POL-0030](POL-0030-constexpr-what-you-can.md) |

## Templates and generic programming

| Rule | Title | Policy |
|------|-------|--------|
| [T.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-raise) | Use templates to raise the level of abstraction of code | [POL-0195](POL-0195-templatize-on-the-third-caller.md) |
| [T.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-algo) | Use templates to express algorithms that apply to many argument types | [POL-0195](POL-0195-templatize-on-the-third-caller.md) |
| [T.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-cont) | Use templates to express containers and ranges | [POL-0195](POL-0195-templatize-on-the-third-caller.md) |
| [T.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-expr) | Use templates to express syntax tree manipulation | [POL-0197](POL-0197-no-expression-templates.md) |
| [T.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-generic-oo) | Combine generic and OO techniques to amplify their strengths, not their costs | [POL-0198](POL-0198-generic-and-dynamic-stay-separate.md) |
| [T.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-concepts) | Specify concepts for all template arguments | [POL-0199](POL-0199-constrain-every-template-parameter.md) |
| [T.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-std-concepts) | Whenever possible use standard concepts | [POL-0199](POL-0199-constrain-every-template-parameter.md) |
| [T.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-auto) | Prefer concept names over `auto` for local variables | [POL-0123](POL-0123-auto-where-the-type-is-redundant.md) |
| [T.13](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-shorthand) | Prefer the shorthand notation for simple, single-type argument concepts | [POL-0199](POL-0199-constrain-every-template-parameter.md) |
| [T.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-low) | Avoid "concepts" without meaningful semantics | [POL-0200](POL-0200-concepts-name-semantics.md) |
| [T.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-complete) | Require a complete set of operations for a concept | [POL-0200](POL-0200-concepts-name-semantics.md) |
| [T.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-axiom) | Specify axioms for concepts | [POL-0200](POL-0200-concepts-name-semantics.md) |
| [T.23](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-refine) | Differentiate a refined concept from its more general case by adding new use patterns. | [POL-0200](POL-0200-concepts-name-semantics.md) |
| [T.24](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-tag) | Use tag classes or traits to differentiate concepts that differ only in semantics. | [POL-0202](POL-0202-tag-types-for-semantic-difference.md) |
| [T.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-not) | Avoid complementary constraints | [POL-0201](POL-0201-no-complementary-constraints.md) |
| [T.26](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-use) | Prefer to define concepts in terms of use-patterns rather than simple syntax | [POL-0200](POL-0200-concepts-name-semantics.md) |
| [T.40](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-fo) | Use function objects to pass operations to algorithms | [POL-0203](POL-0203-function-objects-to-algorithms.md) |
| [T.41](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-essential) | Require only essential properties in a template's concepts | [POL-0200](POL-0200-concepts-name-semantics.md) |
| [T.42](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-alias) | Use template aliases to simplify notation and hide implementation details | [POL-0204](POL-0204-aliases-are-using-declarations.md) |
| [T.43](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-using) | Prefer `using` over `typedef` for defining aliases | [POL-0204](POL-0204-aliases-are-using-declarations.md) |
| [T.44](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-deduce) | Use function templates to deduce class template argument types (where feasible) | [POL-0205](POL-0205-deduce-through-a-factory.md) |
| ~~[T.46](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-regular)~~ | ~~(removed)~~ | removed from the Core Guidelines |
| [T.47](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-visible) | Avoid highly visible unconstrained templates with common names | [POL-0206](POL-0206-no-unconstrained-templates-with-common-names.md) |
| [T.48](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-concept-def) | If your compiler does not support concepts, fake them with `enable_if` | [POL-0199](POL-0199-constrain-every-template-parameter.md) |
| [T.49](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-erasure) | Where possible, avoid type-erasure | [POL-0198](POL-0198-generic-and-dynamic-stay-separate.md) |
| [T.60](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-depend) | Minimize a template's context dependencies | [POL-0207](POL-0207-minimize-template-context-dependencies.md) |
| [T.61](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-scary) | Do not over-parameterize members (SCARY) | [POL-0208](POL-0208-do-not-over-parameterize.md) |
| [T.62](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-nondependent) | Place non-dependent class template members in a non-templated base class | [POL-0208](POL-0208-do-not-over-parameterize.md) |
| [T.64](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-specialization) | Use specialization to provide alternative implementations of class templates | [POL-0209](POL-0209-specialize-classes-overload-functions.md) |
| [T.65](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-tag-dispatch) | Use tag dispatch to provide alternative implementations of a function | [POL-0209](POL-0209-specialize-classes-overload-functions.md) |
| [T.67](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-specialization2) | Use specialization to provide alternative implementations for irregular types | [POL-0209](POL-0209-specialize-classes-overload-functions.md) |
| [T.68](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-cast) | Use `{}` rather than `()` within templates to avoid ambiguities | [POL-0125](POL-0125-everything-is-initialized.md) |
| [T.69](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-customization) | Inside a template, don't make an unqualified non-member function call unless you intend it to be a customization point | [POL-0102](POL-0102-customization-point-is-an-unqualified-call.md) |
| [T.80](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-hier) | Do not naively templatize a class hierarchy | [POL-0210](POL-0210-templates-and-hierarchies-do-not-mix.md) |
| [T.81](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-array) | Do not mix hierarchies and arrays | [POL-0210](POL-0210-templates-and-hierarchies-do-not-mix.md) |
| [T.82](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-linear) | Linearize a hierarchy when virtual functions are undesirable | [POL-0210](POL-0210-templates-and-hierarchies-do-not-mix.md) |
| [T.83](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-virtual) | Do not declare a member function template virtual | [POL-0210](POL-0210-templates-and-hierarchies-do-not-mix.md) |
| [T.84](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-abi) | Use a non-template core implementation to provide an ABI-stable interface | [POL-0211](POL-0211-non-template-core-for-abi.md) |
| [T.100](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-variadic) | Use variadic templates when you need a function that takes a variable number of arguments of a variety of types | [POL-0055](POL-0055-no-va-arg.md) |
| ~~[T.101](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-variadic-pass)~~ | ~~??? How to pass arguments to a variadic template ???~~ | placeholder, not a rule |
| [T.102](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-variadic-process) | How to process arguments to a variadic template | [POL-0212](POL-0212-variadic-only-for-heterogeneous-arguments.md) |
| [T.103](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-variadic-not) | Don't use variadic templates for homogeneous argument lists | [POL-0212](POL-0212-variadic-only-for-heterogeneous-arguments.md) |
| [T.120](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-metameta) | Use template metaprogramming only when you really need to | [POL-0213](POL-0213-metaprogramming-is-a-last-resort.md) |
| [T.121](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-emulate) | Use template metaprogramming primarily to emulate concepts | [POL-0213](POL-0213-metaprogramming-is-a-last-resort.md) |
| [T.122](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-tmp) | Use templates (usually template aliases) to compute types at compile time | [POL-0213](POL-0213-metaprogramming-is-a-last-resort.md) |
| [T.123](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-fct) | Use `constexpr` functions to compute values at compile time | [POL-0030](POL-0030-constexpr-what-you-can.md) |
| [T.124](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-std-tmp) | Prefer to use standard-library TMP facilities | [POL-0213](POL-0213-metaprogramming-is-a-last-resort.md) |
| [T.125](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-lib) | If you need to go beyond the standard-library TMP facilities, use an existing library | [POL-0213](POL-0213-metaprogramming-is-a-last-resort.md) |
| [T.140](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-name) | If an operation can be reused, give it a name | [POL-0029](POL-0029-named-operation.md) |
| [T.141](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-lambda) | Use an unnamed lambda if you need a simple function object in one place only | [POL-0035](POL-0035-lambda-only-for-glue.md) |
| [T.143](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-non-generic) | Don't write unintentionally non-generic code | [POL-0214](POL-0214-no-accidentally-non-generic-code.md) |
| [T.144](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-specialize-function) | Don't specialize function templates | [POL-0209](POL-0209-specialize-classes-overload-functions.md) |
| [T.150](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-check-class) | Check that a class matches a concept using `static_assert` | [POL-0215](POL-0215-static-assert-the-concept.md) |

## C-style programming

| Rule | Title | Policy |
|------|-------|--------|
| [CPL.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcpl-c) | Prefer C++ to C | [POL-0216](POL-0216-c-code-enters-through-a-wrapper.md) |
| [CPL.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcpl-subset) | If you must use C, use the common subset of C and C++, and compile the C code as C++ | [POL-0216](POL-0216-c-code-enters-through-a-wrapper.md) |
| [CPL.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rcpl-interface) | If you must use C for interfaces, use C++ in the calling code using such interfaces | [POL-0216](POL-0216-c-code-enters-through-a-wrapper.md) |

## Source files

| Rule | Title | Policy |
|------|-------|--------|
| ~~[SF.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-file-suffix)~~ | ~~Use a `.cpp` suffix for code files and `.h` for interface files if your project doesn't already follow another convention~~ | coding standard — file extensions |
| [SF.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-inline) | A header file must not contain object definitions or non-inline function definitions | [POL-0217](POL-0217-headers-declare-sources-define.md) |
| [SF.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-declaration-header) | Use header files for all declarations used in multiple source files | [POL-0217](POL-0217-headers-declare-sources-define.md) |
| ~~[SF.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-include-order)~~ | ~~Include header files before other declarations in a file~~ | coding standard — include order and form |
| ~~[SF.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-consistency)~~ | ~~A `.cpp` file must include the header file(s) that defines its interface~~ | coding standard — include order and form |
| ~~[SF.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-using)~~ | ~~Use `using namespace` directives for transition, for foundation libraries (such as `std`), or within a local scope (only)~~ | coding standard — `using namespace` placement |
| ~~[SF.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-using-directive)~~ | ~~Don't write `using namespace` at global scope in a header file~~ | coding standard — `using namespace` placement |
| ~~[SF.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-guards)~~ | ~~Use `#include` guards for all header files~~ | coding standard — include guards |
| [SF.9](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-cycles) | Avoid cyclic dependencies among source files | [POL-0218](POL-0218-dependencies-form-a-dag.md) |
| ~~[SF.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-implicit)~~ | ~~Avoid dependencies on implicitly `#include`d names~~ | coding standard — include order and form |
| ~~[SF.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-contained)~~ | ~~Header files should be self-contained~~ | coding standard — include order and form |
| ~~[SF.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-incform)~~ | ~~Prefer the quoted form of `#include` for files relative to the including file and the angle bracket form everywhere else~~ | coding standard — include order and form |
| ~~[SF.13](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-portable-header-id)~~ | ~~Use portable header identifiers in `#include` statements~~ | coding standard — include order and form |
| ~~[SF.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-namespace)~~ | ~~Use `namespace`s to express logical structure~~ | coding standard — directory and namespace layout |
| ~~[SF.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-unnamed)~~ | ~~Don't use an unnamed (anonymous) namespace in a header~~ | coding standard — anonymous namespace |
| ~~[SF.22](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-unnamed2)~~ | ~~Use an unnamed (anonymous) namespace for all internal/non-exported entities~~ | coding standard — anonymous namespace |

## Standard library

| Rule | Title | Policy |
|------|-------|--------|
| [SL.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-lib) | Use libraries wherever possible | [POL-0013](POL-0013-standard-library-first.md) |
| [SL.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-sl) | Prefer the standard library to other libraries | [POL-0013](POL-0013-standard-library-first.md) |
| [SL.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#sl-std) | Do not add non-standard entities to namespace `std` | [POL-0220](POL-0220-no-additions-to-namespace-std.md) |
| [SL.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#sl-safe) | Use the standard library in a type-safe manner | [POL-0221](POL-0221-type-safe-standard-library-use.md) |

## Standard library — containers

| Rule | Title | Policy |
|------|-------|--------|
| [SL.con.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-arrays) | Prefer using STL `array` or `vector` instead of a C array | [POL-0128](POL-0128-fixed-size-local-sequence.md) |
| [SL.con.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-vector) | Prefer using STL `vector` by default unless you have a reason to use a different container | [POL-0222](POL-0222-vector-by-default.md) |
| [SL.con.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-bounds) | Avoid bounds errors | [POL-0139](POL-0139-no-range-checks-at-use.md) |
| [SL.con.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-copy) | don't use `memset` or `memcpy` for arguments that are not trivially-copyable | [POL-0087](POL-0087-no-memcpy-over-objects.md) |

## Standard library — strings

| Rule | Title | Policy |
|------|-------|--------|
| [SL.str.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-string) | Use `std::string` to own character sequences | [POL-0223](POL-0223-own-with-string-refer-with-view.md) |
| [SL.str.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-view) | Use `std::string_view` or `gsl::span<char>` to refer to character sequences | [POL-0223](POL-0223-own-with-string-refer-with-view.md) |
| [SL.str.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-zstring) | Use `zstring` or `czstring` to refer to a C-style, zero-terminated, sequence of characters | [POL-0043](POL-0043-c-string-converted-on-entry.md) |
| [SL.str.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-charp) | Use `char*` to refer to a single character | [POL-0223](POL-0223-own-with-string-refer-with-view.md) |
| [SL.str.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-byte) | Use `std::byte` to refer to byte values that do not necessarily represent characters | [POL-0223](POL-0223-own-with-string-refer-with-view.md) |
| [SL.str.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-locale) | Use `std::string` when you need to perform locale-sensitive string operations | [POL-0223](POL-0223-own-with-string-refer-with-view.md) |
| [SL.str.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-span) | Use `gsl::span<char>` rather than `std::string_view` when you need to mutate a string | [POL-0223](POL-0223-own-with-string-refer-with-view.md) |
| [SL.str.12](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-s) | Use the `s` suffix for string literals meant to be standard-library `string`s | [POL-0223](POL-0223-own-with-string-refer-with-view.md) |

## Standard library — iostream

| Rule | Title | Policy |
|------|-------|--------|
| [SL.io.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rio-low) | Use character-level input only when you have to | [POL-0194](POL-0194-reading-validates.md) |
| [SL.io.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rio-validate) | When reading, always consider ill-formed input | [POL-0194](POL-0194-reading-validates.md) |
| [SL.io.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rio-streams) | Prefer `iostream`s for I/O | [POL-0225](POL-0225-no-stream-output-in-library-code.md) |
| [SL.io.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rio-sync) | Unless you use `printf`-family functions call `ios_base::sync_with_stdio(false)` | [POL-0226](POL-0226-no-endl.md) |
| [SL.io.50](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rio-endl) | Avoid `endl` | [POL-0226](POL-0226-no-endl.md) |

## Standard library — C stdlib

| Rule | Title | Policy |
|------|-------|--------|
| [SL.C.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rclib-jmp) | Don't use setjmp/longjmp | [POL-0193](POL-0193-no-setjmp.md) |

## Architectural ideas

| Rule | Title | Policy |
|------|-------|--------|
| [A.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ra-stable) | Separate stable code from less stable code | [POL-0219](POL-0219-reusable-parts-become-libraries.md) |
| [A.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ra-lib) | Express potentially reusable parts as a library | [POL-0219](POL-0219-reusable-parts-become-libraries.md) |
| [A.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ra-dag) | There should be no cycles among libraries | [POL-0218](POL-0218-dependencies-form-a-dag.md) |

## Naming and layout

| Rule | Title | Policy |
|------|-------|--------|
| ~~[NL.1](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments)~~ | ~~Don't say in comments what can be clearly stated in code~~ | coding standard — what a comment carries |
| ~~[NL.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments-intent)~~ | ~~State intent in comments~~ | coding standard — what a comment carries |
| ~~[NL.3](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-comments-crisp)~~ | ~~Keep comments crisp~~ | coding standard — what a comment carries |
| ~~[NL.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-indent)~~ | ~~Maintain a consistent indentation style~~ | coding standard — indentation and brace style |
| ~~[NL.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name-type)~~ | ~~Avoid encoding type information in names~~ | coding standard — case table |
| ~~[NL.7](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name-length)~~ | ~~Make the length of a name roughly proportional to the length of its scope~~ | coding standard — name length against scope |
| ~~[NL.8](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-name)~~ | ~~Use a consistent naming style~~ | coding standard — case table |
| ~~[NL.9](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-all-caps)~~ | ~~Use `ALL_CAPS` for macro names only~~ | coding standard — case table |
| ~~[NL.10](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-camel)~~ | ~~Prefer `underscore_style` names~~ | coding standard — case table |
| ~~[NL.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-literals)~~ | ~~Make literals readable~~ | coding standard — literal readability |
| ~~[NL.15](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-space)~~ | ~~Use spaces sparingly~~ | coding standard — whitespace |
| ~~[NL.16](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-order)~~ | ~~Use a conventional class member declaration order~~ | coding standard — class member declaration order |
| ~~[NL.17](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-knr)~~ | ~~Use K&R-derived layout~~ | coding standard — indentation and brace style |
| ~~[NL.18](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-ptr)~~ | ~~Use C++-style declarator layout~~ | coding standard — declarator layout |
| ~~[NL.19](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-misread)~~ | ~~Avoid names that are easily misread~~ | coding standard — unit suffixes |
| ~~[NL.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-stmt)~~ | ~~Don't place two statements on the same line~~ | coding standard — one thing per line |
| ~~[NL.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-dcl)~~ | ~~Declare one name (only) per declaration~~ | coding standard — one thing per line |
| ~~[NL.25](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-void)~~ | ~~Don't use `void` as an argument type~~ | coding standard — empty argument lists |
| ~~[NL.26](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-const)~~ | ~~Use conventional `const` notation~~ | coding standard — `const` notation |
| ~~[NL.27](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-file-suffix)~~ | ~~Use a `.cpp` suffix for code files and `.h` for interface files~~ | coding standard — file extensions |

