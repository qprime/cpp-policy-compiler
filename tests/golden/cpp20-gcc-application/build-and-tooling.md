cpp20-gcc-application › Build and tooling

Read when: setting up or changing a project's build — warnings, sanitizers, static analysis, formatting, the standard declaration.

## MUST — Warnings are errors, and the set is fixed

POL-0089

Every target compiles under `-Wall -Wextra -Wpedantic -Wconversion
-Wsign-conversion -Werror`. `-Werror=switch` is additionally load-bearing rather
than stylistic on a C++11 project, because it is what makes closed-set
exhaustiveness a compile error there (POL-0033).

A per-site disable is permitted and carries a comment stating why, next to the
pragma. A disable without one is indistinguishable from a warning somebody could
not fix.

The conversion warnings are the two most often removed and the two worth most.
Narrowing and sign-changing conversions are silent at the language level and
produce wrong values rather than diagnostics, which is exactly the class this
corpus treats as undefined behaviour's quieter neighbour (POL-0019).

A warning that does not stop the build is a message in a stream nobody reads,
and the number of them only goes up, so the signal is gone by the second week.
Making them errors keeps the count at zero, which is the only count at which a
new one is visible. The set is fixed rather than chosen per project because a
project that picks its own set picks it by removing whatever is currently
failing, and what is currently failing is the interesting part.

## MUST — The tests run under sanitizers in at least one configuration

POL-0090

UBSan and ASan are enabled in at least one build configuration, and the test
suite runs under it. TSan is added in its own configuration once the project
introduces concurrency.

A sanitizer finding is a defect, and it is a defect of the code rather than of
the configuration. Suppressions are for known issues in third-party code, listed
in a file, each with a reason.

TSan is separate rather than combined because it does not compose with ASan, and
running it before there is concurrency to find reports nothing while costing
every run.

Undefined behaviour is forbidden (POL-0019), and the compiler cannot report most
of it: the whole point of the category is that the standard imposes no
requirement, so a conforming implementation may produce code that appears to
work. That leaves a rule with no mechanism behind it, which is what the
sanitizers supply. They are also the only check here that finds a defect the
author did not think to look for, since they observe what the program actually
did rather than what it was expected to do.

## MUST — Static analysis runs a fixed set of check families

POL-0091

`clang-tidy` runs with `bugprone-*`, `cert-*`, `cppcoreguidelines-*`,
`performance-*`, and `readability-*`.

Disables are project-level, live in `.clang-tidy`, and carry one comment per
disable stating why. A disable list with no comments is a record of what was
inconvenient, not of what was decided.

Per-site `NOLINT` is for the case the check cannot see, and it names the check
it suppresses rather than suppressing everything at that line.

Static analysis is the layer between the compiler and a reader: it finds the
patterns that are well-formed, so no warning applies, and wrong often enough to
be worth naming. Most of what it reports here is already a policy in this
corpus, which is the reason the families are fixed — the check set is the
mechanical half of guidance that otherwise has to be remembered. Choosing the
families per project would let the set drift away from the policies it is
supposed to enforce, and nothing would report that it had.

The tool is due diligence and not how quality is produced. A codebase that
needs its linter in order to be well designed is not well designed; the linter
catches what slipped.

## MUST — Formatting is decided once per project and applied by the tool

POL-0092

Every project has a `clang-format` configuration, committed, and every file
conforms to it. The baseline is `BasedOnStyle: Google` with `IndentWidth: 4` and
`ColumnLimit: 100`.

Details beyond the baseline are a per-project choice. That there is a
configuration, and that it is applied rather than approximated by hand, is not.

Formatting is not a matter of judgment once the file is committed, so it is the
one part of a convention that should never be discussed again. A tool applies it
in full, which is what makes that possible.

An unformatted or hand-formatted tree makes every diff carry changes nobody
made. Reformatting noise buries the change under review, and it makes the
history useless for the question of when a line last actually changed. The
baseline is stated rather than left open because a project with no configuration
does not stay unformatted, it acquires several formats, one per author, and
converging afterward costs a commit that touches every file.

## MUST — The language standard is declared once, in the build configuration

POL-0093

One declaration, in the top-level build configuration, and every target inherits
it. Reaching for a feature from a later standard than the one declared is a
defect, not an upgrade.

The reverse is also a defect. Using an older mechanism on a project that
declared a newer standard — a stream where `std::format` exists, an iterator
pair where `std::span` exists, `enable_if` where concepts exist — is the same
mistake in the other direction.

Every per-standard column in this corpus reads against this declaration. The
policy that says which spelling to use has no answer without it.

The declaration is what makes the mechanism guidance decidable at all: a rule of
the form "use the optional for your standard" needs a standard, and a project
that never stated one has to infer it from what currently compiles. A single
declaration also keeps the answer uniform across targets, which matters because
a feature that compiles in one target and not another produces a build failure
attributed to the target rather than to the version drift that caused it.

## MUST — The code is ISO standard C++, not a dialect of it

POL-0158 · CG P.2, CG CPL.1

```cpp
// Never. Compiler extensions, silently accepted, silently non-portable.
typeof(x) y = x;
int values[n];                      // variable-length array
__attribute__((packed)) struct Wire { ... };

// Right.
decltype(x) y = x;
std::vector<int> values(n);
```

`-Wpedantic` under POL-0089 is what reports an extension, and it is on for
exactly this reason. Where a platform genuinely requires one — an alignment
attribute, an intrinsic — it is isolated behind an interface that the rest of
the code sees as ordinary C++, which is the escape hatch POL-0064 describes for
the binding layer.

C constructs are not written where C++ has an equivalent, and this covers the
whole family: C casts (POL-0094), C arrays (POL-0155), macros (POL-0157),
`va_arg` and `setjmp` (POL-0154), `malloc` (POL-0127).

An extension compiles on the compiler it was written against and fails on the
next one, usually years later during a migration nobody budgeted for. It also
defeats POL-0093: the declared standard stops describing what the code needs,
so the build configuration no longer states the truth about the project.

## MUST — A change made for performance carries the measurement that justified it

POL-0172 · CG Per.6

```cpp
// Never. A claim with no referent, and a departure from POL-0004 on its strength.
// Faster than std::unordered_map.
FlatMap<ToolId, Tool> by_id_;

// Right. The number, the workload, and the date.
// Flat layout: 2.4x faster lookup than std::unordered_map at n<=64,
// measured 2026-08-14 on the 12k-move planner benchmark.
FlatMap<ToolId, Tool> by_id_;
```

This is one of the cases POL-0112 admits a comment for: a reason that makes an
otherwise unusual choice legible. Without it the next reader sees a departure
from the boring option (POL-0004) with no way to tell whether it was justified,
and no basis for undoing it.

An unmeasured performance claim is untestable, so it cannot be wrong and cannot
be removed. It accumulates: the codebase fills with complexity that was added
for speed nobody demonstrated and nobody can now argue against.

Most performance rules are deliberately absent from this corpus, because
optimization is code-local and measured rather than decided in advance. This is
the rule that makes that position workable — the measurement is what turns a
local decision into one a later reader can evaluate.
