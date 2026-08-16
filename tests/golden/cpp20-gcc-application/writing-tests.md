cpp20-gcc-application › Writing tests

Read when: writing or reviewing tests — what to test, what not to, goldens, round-trips, the framework.

## SHOULD — Test where the logic lives

POL-0065

A unit test targets the function or the class that holds the logic, not the
pipeline that calls it. A test that drives the whole pipeline to exercise one
branch is an integration test, and integration tests are few.

The test for which kind is being written: name the thing that would be wrong if
the test failed. Where that is one function, the test belongs against that
function. Where it is the composition, the test belongs at the composition and
there are only a handful of those.

A pipeline test that fails names the pipeline. Finding which of its stages is
actually wrong is then a separate investigation, run every time, and it takes
longer than the test did. A pipeline test also passes for the wrong reasons:
one stage compensating for another's error produces correct end-to-end output
from two defects, and the composition is the level at which that is invisible.
Testing at the level of the logic makes a failure name its own cause.

## MUST — Do not test the language or the standard library

POL-0066

No test asserting that a `const` member cannot be assigned, that a default-
constructed optional is empty, that a `unique_ptr` releases on destruction, or
that a `vector` grows when pushed to. Test what this code adds.

```cpp
// Never: this asserts a language guarantee
TEST_CASE("optional is empty by default") { CHECK(!std::optional<int>{}.has_value()); }

// Instead: this asserts something this code decided
TEST_CASE("load_entries returns nullopt for a missing path") {
    CHECK(!load_entries(Path{"does-not-exist"}).has_value());
}
```

The line is whether the assertion could fail without a change to this codebase.
If not, the test is asserting the compiler.

A test of a language guarantee cannot fail, so it contributes no information and
consumes the attention a real test would have received. It also misrepresents
coverage: a suite reporting a hundred passing tests where thirty assert the
standard library looks like a suite that checked thirty things it did not. The
form is worth naming because it is what gets written when the goal is a test
rather than a question about the code.

## MUST — Test the invariant, not the accessor

POL-0067

A validating constructor gets a test for each way its invariant can be violated
(POL-0022). An accessor that returns a member gets none.

```cpp
// Yes: the constructor decided something, and this is what it decided
TEST_CASE("RetryPolicy rejects a non-positive attempt count") {
    CHECK_THROWS_AS(RetryPolicy(0, 100.0, 0.1), std::invalid_argument);
}

// No: this asserts that a member initializer ran
TEST_CASE("max_attempts returns max_attempts") {
    CHECK(RetryPolicy(3, 100.0, 0.1).max_attempts() == 3);
}
```

The rule follows from where the decisions are. A constructor that rejects input
made a choice about what is valid, and that choice is what a later edit can
change without noticing. An accessor made no choice, so a test of it asserts
that the compiler assigned a member.

Accessor tests are cheap to write in bulk, which is why they accumulate, and
every one of them has to be maintained through a rename that a compiler would
have caught anyway. Their real cost is the reading: a suite where most tests
assert nothing trains whoever reads it to skim, and the invariant test that
matters is in the same file.

## MUST — Round-trip tests assert semantic equivalence

POL-0068

A round-trip test asserts `parse(format(model)) == model`. It does not assert
that the text produced matches the text consumed.

Whitespace, key order, quoting style, and equivalent numeric spellings may
legitimately differ, and a test that forbids them is testing the formatter's
current output rather than the pair's agreement.

Where the model has no equality operator, the comparison is against a normalized
form, defined once and used by every round-trip test rather than restated per
test.

Comparing text asserts a property neither function promised, so it fails on
changes that are correct and passes on changes that are not. A formatter that
starts emitting two spaces breaks it, which is a false alarm that trains whoever
sees it to regenerate the expectation rather than read it. Meanwhile a parser
that drops a field the formatter never emits leaves the text identical and the
model wrong, which is the defect the round trip existed to catch.

## MUST — One assertion of a behaviour

POL-0069

Two tests covering the same behaviour over the same input are a defect, not
redundancy. Before adding a test, find whether the behaviour is already
asserted; before adding a test file, find whether one exists for the unit.

Coverage is a question about behaviours, not about test count. A second test of
a covered behaviour raises the count and covers nothing.

The duplicate does not stay a duplicate. One copy gets updated when the
behaviour changes and the other does not, which leaves a suite asserting two
contradictory things about one input; whichever fails first is treated as the
broken one, and there is no way to tell from the tests which was right.
Duplicates also cost every future change twice, so the suite gets slower to
maintain in proportion to how thoroughly it was duplicated. The cost falls
hardest on generated tests, which are written from the code rather than from a
list of what is already asserted.

## MUST — Use the project's test framework

POL-0070

Tests use the framework the project declared — Catch2, GoogleTest, or doctest.
No hand-rolled `int main()` runner, no `PASS` and `FAIL` prints, no manual
counting of results.

```cpp
// Never
int main() {
    if (checksum(bytes) != expected) { std::cout << "FAIL\n"; return 1; }
    std::cout << "PASS\n";
}

// Instead
TEST_CASE("checksum matches the known vector") {
    CHECK(checksum(bytes) == expected);
}
```

Which framework is a per-project choice. That there is one is not.

A hand-rolled runner has no discovery, no filtering, no per-case isolation, and
no machine-readable output, so it cannot be run selectively while debugging and
cannot be aggregated with the rest of the suite. It also fails open: a case that
throws takes the process down before the later cases run, and the report says
nothing about the cases that never executed. The framework is where all of that
is already solved, which is why writing around it produces a suite that costs
more and reports less.

## MUST — Structured output is golden-tested

POL-0071

Any computation producing structured output — a plan, a schedule, a trace, an
intermediate representation, generated code — has a golden test over that
output.

Every change then lands as exactly one of two things:

- **no golden diff**, which is what proves a change was a refactor
- **a deliberate regeneration**, whose diff is explained in the commit message

A diff that is neither is a change whose effect nobody has stated. Regenerating
goldens to make a build pass, without the explanation, discards the only record
of what the change did.

Adding an alternative to a shared structure is versioned and moves everything
together (POL-0063).

Golden tests require the output to be reproducible, which is why POL-0019 is
their precondition rather than a separate concern.

Structured output is too large to assert by hand and too small a change to
notice by eye, so without a golden there is no level at which a modification is
reviewable. The golden converts "I believe this refactor changed nothing" from
a claim into a diff, and it is the only mechanism here that catches an unintended
change whose shape nobody predicted. That is also why the explained-regeneration
half is not optional: an unexplained regeneration has the same diff as an
undetected defect.

## MUST — Include a test that would fail on a plausible wrong implementation

POL-0072

A suite where every test passes against a plausible wrong implementation is not
testing. For each unit, name the wrong version somebody could reasonably have
written, and include the case that distinguishes it.

```cpp
// A checksum that ignores its input passes this
CHECK(checksum(bytes).size() == 32);

// It does not pass this
CHECK(checksum(bytes) != checksum(other_bytes));
```

The wrong implementations worth defeating are the near ones: the off-by-one
boundary, the empty input, the ignored parameter, the swapped pair of arguments
(POL-0016). Not an implementation that returns nothing at all.

Tests written from the code inherit the code's assumptions, so they assert what
the implementation does rather than what it was required to do, and they pass by
construction. That failure mode leaves no trace: the suite is green, the count is
high, and the one thing missing is any case whose outcome was in doubt. Choosing
the wrong implementation first is what makes the test an experiment rather than a
transcript.
