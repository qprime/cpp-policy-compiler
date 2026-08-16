cpp20-gcc-application › Writing an expression

Read when: writing the line itself — casts, arithmetic and signedness, which standard-library facility to reach for, how text gets formatted.

## MUST — A cast is named, and the named cast is nearly always `static_cast`

POL-0094 · CG ES.48, CG ES.49, CG Type.1

```cpp
// Never. Which conversion is this? The syntax does not say.
double ratio = (double)count / (double)total;
Widget* w = (Widget*)handle;

// Right.
const auto ratio = static_cast<double>(count) / static_cast<double>(total);
auto* w = static_cast<Widget*>(handle);
```

`const_cast`, `reinterpret_cast`, and `dynamic_cast` each defeat a guarantee
the reader is entitled to assume, so each carries a comment stating why.
`static_cast` needs none.

Before writing any cast, check whether the type upstream is wrong. A cast is an
assertion that the type system has it backwards, and most casts mark a
representation chosen badly rather than a conversion genuinely needed
(POL-0034).

A C-style cast selects from among `static_cast`, `const_cast`, and
`reinterpret_cast` by rules almost nobody has memorized. The same four
characters mean a checked numeric conversion on one line and a reinterpretation
of raw memory on the next, and nothing in the syntax distinguishes them. A
named cast says which one it is and can be searched for when the class of
conversion turns out to be the defect.

## NEVER — Never cast away const, and never reinterpret an object's bytes through a pointer

POL-0095 · CG ES.50, CG Type.1

```cpp
// Never. If the referent is genuinely const, the write is undefined behaviour.
void touch(const Config& cfg) {
    const_cast<Config&>(cfg).retries = 3;
}

// Never. Type-punning through a pointer cast breaks strict aliasing.
const float bits = *reinterpret_cast<const float*>(&raw_word);
```

If a function needs to modify what it was given, it takes a non-const
reference and says so in its signature. If bytes genuinely need
reinterpreting, use `std::bit_cast` on C++20 and `std::memcpy` before it; both
are defined and both optimize to the same instruction.

`const_cast` compiles identically whether or not the original object was
declared const, so the undefined case and the merely-ugly case are
indistinguishable at the point the cast is written. The alias violation is
worse: it produces a program that behaves correctly at low optimization levels
and changes behaviour when the optimizer is turned up, which places the failure
in the build configuration rather than in the line that caused it (POL-0019).

## MUST — Arithmetic is done in a signed type

POL-0101 · CG ES.102, CG ES.103, CG ES.106

```cpp
// Never. If margin exceeds width, the result is enormous, not negative.
const std::size_t slack = sheet.width_mm() - margin_mm;

// Right.
const auto slack = static_cast<std::int64_t>(sheet.width_mm()) - margin_mm;
```

`std::size_t` holds a size or an index that came from the standard library, and
converts to a signed type once, at the point the arithmetic starts. Letting an
unsigned type spread outward from `size()` is how the wrap reaches code that
does no container work.

Never rely on signed overflow either. It is undefined, so the optimizer assumes
it cannot happen and deletes the check written to detect it.

Unsigned arithmetic wraps at zero, so a subtraction that should go negative
produces a very large positive number instead. The comparison written to catch
it then succeeds, which means the guard and the defect cancel out and the wrong
value flows on. Nothing reports it: the wrap is defined behaviour, so no
sanitizer fires and no warning applies. A signed type makes the same
subtraction produce a negative number, which every subsequent check treats as
the error it is (POL-0002).

## NEVER — Never compare a signed value with an unsigned one

POL-0102 · CG ES.100

```cpp
// Never. offset converts to unsigned; a negative offset passes the guard.
int offset = compute_offset();
if (offset < path.size()) { use(path[offset]); }

// Right. One type, and the negative case is caught.
const auto count = static_cast<std::int64_t>(path.size());
if (offset >= 0 && offset < count) { use(path[static_cast<std::size_t>(offset)]); }
```

The fix is the type, not a cast at the comparison. A cast that silences the
warning keeps the defect and removes the diagnostic.

The signed operand converts to unsigned before the comparison, which turns
`-1 < 1u` into false. A bounds check written against a negative index therefore
admits it, and the indexing that follows reads out of bounds. `-Wsign-compare`
under POL-0089 makes this a build error, which is the only reason it is
survivable at all — the line reads correctly in every language the author might
be coming from, and it does not mean what it says here.

## SHOULD — Reach for the standard library before writing the facility yourself

POL-0109 · CG SL.1, CG SL.2

```cpp
// Avoid. A hand-rolled split is code to review, test, and carry forever.
std::vector<std::string> split(const std::string& s, char sep);

// Prefer, on C++20.
for (const auto part : std::views::split(text, ',')) { use(part); }
```

Where the standard has no answer, take the project's existing dependency
before adding a new one, and write the facility only when neither has it.

A C-library facility is never the answer where a C++ one exists: `qsort` takes
a `void*` comparator that defeats type checking and inlining, `strcpy` has no
bound, and `rand` has no distribution guarantee worth relying on.

A hand-written equivalent has to be reviewed, tested, and maintained, and it
will not match the standard version at the edges nobody wrote a test for —
empty input, a single element, self-assignment, an allocation that throws
partway. The standard version has those settled and has had them exercised by
every program that ever ran.

## NEVER — Never use a facility a later standard superseded

POL-0110 · CG SL.io.50

| Never | Since | Use instead |
|-------|-------|-------------|
| `std::auto_ptr` | C++11 | `std::unique_ptr` |
| `std::bind` | C++11 | a lambda |
| `throw()` exception specification | C++11 | `noexcept` |
| `NULL`, or `0` as a null pointer | C++11 | `nullptr` |
| `register` | C++11 | *(delete it)* |
| `std::random_shuffle` | C++11 | `std::shuffle` |
| `std::endl` where `'\n'` will do | any | `'\n'` |
| `std::ostringstream` to format a number | C++20 | `std::format` |
| `enable_if` SFINAE for a constraint | C++20 | a concept or `requires` |
| Compound assignment on `volatile` | C++20 | `std::atomic` |
| A third-party `expected` | C++23 | the project's result type until `std::expected` |

`std::endl` flushes, which turns a loop of writes into a loop of system calls
for no effect the author intended.

Every entry here remains legal, which is the reason the list exists. A
generator's training weights decades of code that predates the replacement, so
these are what it produces by default and nothing in the build objects. Each
has a direct modern equivalent that is shorter, safer, or both, so the
replacement costs nothing but knowing which one it is (POL-0093).

## MUST — Text is formatted by a format call, not assembled on a stream

POL-0111

```cpp
// Never. Manipulators persist on the stream past the line that set them.
std::ostringstream out;
out << std::fixed << std::setprecision(2) << "width " << width_mm << "mm";

// Right, on C++20.
const auto text = std::format("width {:.2f}mm", width_mm);
```

Below C++20 the spelling is one contained helper holding an
`std::ostringstream`, or `snprintf` into a fixed buffer where a real-time loop
forbids allocation (POL-0012). On C++20 an `std::ostringstream` in new code is
a defect.

`printf`-family calls are not type-safe. They are permitted only where a
project has no `std::format` and a measured reason to avoid streams.

A stream carries formatting state, so `std::setprecision` set for one value
applies to every value written afterward, including from a different function
that shares the stream. The defect appears as a number formatted wrongly a long
way from the manipulator that caused it. A format string states the formatting
for each argument at the point of use and carries nothing between calls.
