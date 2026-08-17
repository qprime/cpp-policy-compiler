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

## NEVER — Never define a macro for a constant, a function, or program text

POL-0157 · CG ES.30, CG ES.31, CG ES.33

```cpp
// Never. No type, no scope, and MIN(i++, j) evaluates i++ twice.
#define MAX_TOOLS 64
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// Right.
constexpr int kMaxTools = 64;
constexpr auto smaller = [](auto a, auto b) { return std::min(a, b); };
```

A constant is `constexpr` (POL-0010), a function is a function or a `constexpr`
function (POL-0036), and a compile-time choice is `if constexpr` rather than
`#if`.

The exceptions are an include guard (POL-0028) and the small set of macros a
platform or test framework requires. Those are `ALL_CAPS` and project-prefixed,
per POL-0084, precisely because they have no scope and a short name will collide.

A macro is a textual substitution performed before the compiler sees a type, so
it obeys no scope, appears in no diagnostic, and is invisible to the debugger.
An argument used twice in the body is evaluated twice, which turns any argument
with a side effect into a defect that the call site cannot see.

`ALL_CAPS` is reserved for macros for this reason: the name is the only warning a
reader gets that ordinary language rules do not apply on that line.

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

## MUST — Every variable is initialized at its declaration, with braces

POL-0096 · CG ES.20, CG ES.23

```cpp
// Never. Indeterminate between the two lines, and reading it there is UB.
int retries;
retries = policy.retries;

// Right. Braces also reject the narrowing conversion.
const int retries{policy.retries};
const double ratio{0.75};
```

Braces are the default because they refuse narrowing: `int n{3.7}` fails to
build where `int n(3.7)` silently truncates.

Use parentheses where braces would select a `std::initializer_list`
constructor you did not want. `std::vector<int> v{10}` holds one element and
`std::vector<int> v(10)` holds ten, which is the one case where the brace
default is a trap rather than a guard.

A variable declared without a value has a window in which it holds whatever was
on the stack, and reading it is undefined behaviour rather than a wrong value.
No warning catches it reliably, because the compiler cannot see across the
branch that was supposed to assign it. Initializing at the declaration removes
the window rather than narrowing it, and it forces the value's origin to be
visible on the line that introduces the name (POL-0026).

## SHOULD — A variable is declared where it is first used

POL-0097 · CG ES.21, CG ES.22

```cpp
// Avoid. Three names live and meaningless for most of the function.
Plan plan;
double total;
std::string label;
// ... forty lines that do not touch them ...

// Prefer.
const auto plan = build_plan(input);
const auto total = plan.total_mm();
```

Where a value must outlive a branch that computes it, prefer an immediately
invoked helper or a function that returns it over declaring it early and
assigning it later, so it can still be `const` (POL-0020).

A variable declared before it means anything has a region of the function in
which it is live and carries nothing. That region is where a stale read
happens, and it grows every time the function does. Declaring at first use
makes the scope match the meaning, which is also what lets the declaration be
`const` and what makes an unused value visible rather than merely inert.

## MUST — One name per declaration, written in the C++ form

POL-0153 · CG ES.10, CG NL.11, CG NL.18, CG NL.21, CG NL.25

```cpp
// Never. Only p is a pointer, and the initializers are easy to misread.
int* p, q;
const long timeout = 3600000;
void reset(void);

// Right.
int* p{nullptr};
int q{0};
constexpr auto kTimeoutMs = 3'600'000L;
void reset();
```

The declarator binds to the type, not the name: `int* p` rather than `int *p`,
because the pointer is part of what `p` is. An empty parameter list is written
`()`, never `(void)`, which is the C spelling.

Long numeric literals use digit separators, and a literal whose type matters
carries its suffix — `3'600'000L`, `0.5F`, `1U`. A literal that means something
gets a name instead (POL-0010).

A multi-name declaration distributes the declarator across names unevenly, so
`int* p, q` declares one pointer and one `int` while reading as two pointers. It
also blocks the per-name initialization POL-0096 requires, since the natural
form initializes only the last one, and it makes every later edit that adds a
name inherit whichever declarator happened to be there.

## MUST — A local name is never reused and never shadows an outer one

POL-0165 · CG ES.12, CG ES.26

```cpp
// Never. count means two things, and the inner tool hides the outer one.
int count = tools.size();
count = failures.size();

for (const auto& tool : tools) {
    for (const auto& tool : tool.inserts()) { check(tool); }
}

// Right.
const auto tool_count = tools.size();
const auto failure_count = failures.size();

for (const auto& tool : tools) {
    for (const auto& insert : tool.inserts()) { check(insert); }
}
```

A variable holds one thing for its whole life. Reusing it for a second purpose
is two variables sharing storage, and it is what blocks the `const` POL-0020
asks for.

Shadowing compiles silently, so an edit to the inner block that meant to touch
the outer name touches the inner one instead, and the outer value is simply
never updated. `-Wshadow` reports it, which is why the warning set in POL-0089
is worth having.

Both are the same defect at different scales: a name that does not identify one
value forces the reader to track which meaning is live at each line, and the
declaration no longer answers what the name is (POL-0097).
