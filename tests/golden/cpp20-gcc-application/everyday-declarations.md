cpp20-gcc-application › Everyday declarations

Read when: declaring anything — `const`, named constants, initialization, determinism.

## MUST — No magic constants

POL-0010 · CG ES.45

An inline literal that carries meaning gets a name. `constexpr` at file scope
for a value one translation unit owns; a shared constants header for a value
several modules must agree on.

```cpp
constexpr double kMinSpacingMm = 10.0;
if (spacing_mm < kMinSpacingMm) { ... }
```

The test is whether the number would ever be changed on its own. If it would, it
has a name. Trivially obvious literals do not: `0`, `1`, `0.5` for a midpoint,
array indices, and identity values in arithmetic.

Unnamed literals in limit checks, timing, and dimensional arithmetic drift and
diverge. The same threshold gets written at three sites, one is updated, and the
disagreement is invisible because nothing connects the three. The name is also
what states the unit and the intent, which the literal cannot.

## MUST — No undefined behaviour, no run-to-run variation

POL-0019 · CG P.4, CG ES.20

Four things are defects, each on its own:

- undefined behaviour of any kind, whatever the observed result
- unordered-container iteration order reaching output
- reading an object before it is initialized
- platform-dependent floating-point in output that is compared

Where iteration order reaches output, the fix is an ordered container or an
explicit sort at the point of emission, not a hash seed that happens to be
stable. Where floating-point reaches compared output, the fix is a stated
tolerance or a fixed-precision rendering, not a hope that two toolchains agree.

Every object is initialized at the point of declaration. `const` (POL-0020)
forces this, which is one more reason it is the default.

Undefined behaviour is not a wrong answer, it is the absence of any contract
about the answer. Code that appears to work under one compiler, one
optimization level, and one input has not been shown to work at all; it has been
shown not to have been caught. Run-to-run variation costs the same thing from
the other direction: an output that differs between runs cannot be diffed
against a known-good one, so every mechanism that would have caught the next
defect stops working at once.

## MUST — `const` by default

POL-0020 · CG P.10, CG Con.1, CG Con.2, CG Con.3, CG Con.4, CG Con.5

Four sites, each `const` unless something requires otherwise:

| Site | Form |
|------|------|
| An object that does not change after construction | `const T x = ...;` |
| A member function that does not mutate | trailing `const` |
| A parameter that is only read | `const T&`, or `const T` by value |
| A value known at compile time | `constexpr` |

`constexpr` is the stronger claim and is preferred wherever the value can be
computed at compile time. `inline constexpr` at namespace scope in a header
requires C++17; a C++11 project puts a header constant in an anonymous namespace
or behind a function returning it. C++20 adds `consteval` for the case where
compile-time evaluation is required rather than merely possible.

A `const` member and a private member with a `const` accessor are both
immutable; choose by whether the type has an invariant to protect (POL-0015).

The order in which `const` is decided is the point: it is written first and
removed when a mutation is required, never added once the code is believed
correct. Written the other way, `const` records what happened to be true when
someone last looked, which is not a guarantee anything can rely on. A
non-`const` object tells the reader it changes, so an object that never changes
and is not marked makes that signal a lie everywhere in the file.

## THIS WAY — Write `const` first, remove it when a mutation is required

POL-0026 · CG Con.1, CG Con.5, CG ES.25, CG P.10

The authoring order is the pattern. Every declaration is written `const`, and
`const` comes off only when the code that follows needs to mutate.

```cpp
const Bounds b = bounds_of(records);          // const local
double size_bytes() const { return ...; }     // const member function
void publish(const Payload& payload);         // const parameter
constexpr double kMinFillRatio = 0.5;         // compile-time constant
```

`mutable` exists for a cache that does not participate in the object's observed
value. Anywhere else it is a member that wanted to be non-`const` and was not
declared that way.

POL-0020 states which sites carry `const`. This is how they come to.

Added afterward, `const` records what was true the last time somebody checked,
and the check is skipped exactly on the declarations that were hardest to
reason about. Written first, it is a claim the compiler then verifies, so the
cases where the claim is wrong are the cases that fail to build. The order also
changes what the reader learns from a non-`const` local: it means *this
changes*, and that signal only carries information if the alternative was the
default.
