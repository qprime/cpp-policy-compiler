cpp20-gcc-application › Choosing a representation

Read when: deciding what type holds a piece of data — alternatives, absence, aggregates, inheritance, whether a thing becomes a type at all.

## MUST — Absence is represented, never encoded

POL-0009 · CG F.60, CG P.6

A value that may legitimately not be there is represented by something whose
type says so. Encoding it in the value space instead is POL-0013, which
enumerates the forms that takes.

The intent is universal. The mechanism depends on the standard the project
declares, and reaching for a mechanism from a later column than the declared one
is a defect.

| C++11 | C++17 | C++20 |
|-------|-------|-------|
| No standard mechanism. Two permitted forms: a dedicated `Optional<T>`-alike in the project's support header, or a `bool`-returning `try_*` function with a reference out-parameter at a documented boundary. Pick one per project; do not mix. | `std::optional<T>` | `std::optional<T>` |

Columns group standards where the grouping changes no guidance: the C++11 column
covers C++11 and C++14, the C++20 column covers C++20 and C++23.

Absence is not failure. The optional form means there is legitimately nothing
here. A failure carrying a reason the caller must act on uses the result
mechanism instead, and substituting one for the other discards the reason.

Once absence shares a representation with a legal value, the type system cannot
separate them again, and every site downstream inherits the ambiguity without
any way to detect that it did.

## NEVER — Never encode absence in a sentinel value

POL-0013

NaN meaning *no value*. `-1` meaning *not found*. `""` meaning *unset*. `0`
meaning *unset* on a field where zero is a legal reading. Each takes a value the
type can legitimately hold and overloads it with a second meaning the type
cannot distinguish from the first.

```cpp
// Never: the signature admits -1, so absence flows into arithmetic and indexing
int find_index(const std::vector<Item>& items, Id id);   // -1 when absent
const int i = find_index(items, id);
total += weights[i];                                     // -1 becomes a huge index

// Instead: absence has its own type, and the check cannot be skipped
std::optional<std::size_t> find_index(const std::vector<Item>& items, Id id);
if (const auto i = find_index(items, id)) { total += weights[*i]; }
```

Shown in its C++17 form. POL-0009 carries the positive rule and the mechanism
for each standard. NaN in output is a defect to investigate, never a value with
meaning.

The cost is paid where the two meanings collide, which is never the site that
chose the sentinel. A NaN from a failed computation and a NaN meaning "nothing
here" are the same bits, so the bug and the intent are indistinguishable
everywhere downstream. Sentinels look cheap because they need no new type, and
they are what generation reaches for by default when working from the shape of
the data alone.

## MUST — Closed-set variation is compiler-checked for exhaustiveness

POL-0033 · CG C.181, CG C.182

A value that is one of a fixed set of alternatives is represented so that adding
an alternative breaks compilation at every site that must handle it. Falling
through silently is the defect this rule exists to prevent.

The intent is universal. The mechanism depends on the standard the project
declares.

| C++11 | C++17 | C++20 |
|-------|-------|-------|
| `enum class` tag plus a `switch` with **no `default` label**, compiled under `-Werror=switch`. Payload lives in a struct per alternative and the tagged aggregate is documented as a unit. | `std::variant` plus `std::visit` over an exhaustive overload set | `std::variant` plus `std::visit` |

The C++11 form is not a weaker version of the C++17 one. It obtains the same
guarantee from the warning system rather than from the type system, which is why
`-Werror=switch` is load-bearing rather than stylistic on a C++11 project.

One overload per alternative, never a generic `[](auto&&)` catch-all. A catch-all
compiles for every alternative added later and swallows exactly the case that
was just introduced, which removes the only property the variant was chosen for.

Forbidden in every standard: an `enum` paired with an if/else-if chain, which
obtains no guarantee at all, and a string tag field with optional payload members
(POL-0043).

A missing case is not detectable from the site that is missing it, because
nothing there is wrong. It is detectable only from the set of alternatives, which
lives somewhere else and grows without notifying anybody. Making exhaustiveness a
compile error moves the check from whoever remembers the alternative was added to
the build, which runs against every site every time.

## NEVER — Never dispatch on a string tag

POL-0043

A struct with a `std::string kind` field and optional payload members is a
tagged union with no checking. Nothing constrains the tag to a known value,
nothing ties a payload to the tag that makes it meaningful, and nothing reports
a case that went unhandled.

```cpp
// Never: any string is a legal tag, and no payload is tied to one
struct Event {
    std::string kind;                        // "connect", "send", "close"
    std::optional<std::string> endpoint;
    std::optional<std::size_t> size_bytes;
    std::optional<int> code;
};

// Instead: one alternative per case, each carrying only its own payload
struct Connect { std::string endpoint; };
struct Send    { std::size_t size_bytes; };
struct Close   { int code; };
using Event = std::variant<Connect, Send, Close>;

std::string render(const Event& event) {
    return std::visit(overloaded{
        [](const Connect& e) { return "connect " + e.endpoint; },
        [](const Send& e)    { return "send " + std::to_string(e.size_bytes); },
        [](const Close& e)   { return "close " + std::to_string(e.code); },
    }, event);
}
```

An `enum class` paired with an if/else-if chain is half a fix. The tag becomes a
real type, and nothing still forces the chain to handle every case. Shown in its
C++17 form; POL-0033 carries the mechanism for each declared standard.

The string tag is what generation reaches for when working from example data,
because the data shows a field whose values happen to be strings. Every property
worth having is then absent at once: the set of alternatives is not written down
anywhere, a typo in a tag is a runtime miss rather than a compile error, and a
payload can be present for the wrong tag or absent for the right one. The cost
is paid by whoever adds the fourth alternative and does not find the site that
needed it.

## SHOULD — When a thing becomes a type

POL-0034 · CG C.2

Work down the list. Stop at the first match.

| Question | If yes |
|----------|--------|
| Does it have an invariant — some combination of values that must never exist? | A `class` with a validating constructor (POL-0015, POL-0022) |
| Does it have a *structural* precondition other code wants to assume? | A wrapper type (POL-0027) |
| Is it a fixed set of alternatives? | `enum class`, or a variant when the alternatives carry payloads (POL-0033) |
| Do several values always travel together into functions? | A params struct or an aggregate (POL-0023) |
| Are two same-typed values confusable at a boundary, *and* does arithmetic not flow through them? | A distinct type — a named escape, not the default (POL-0038) |
| None of the above | A primitive with a unit-suffixed name (POL-0017). This is the common case. |

The last row is the answer most of the time, and the list is ordered so that the
cheap answer is reached by elimination rather than by judgment. A question
skipped is a type introduced that carries no constraint, and a type with no
constraint is ceremony.

Every type is an interface somebody has to learn, so the question is never
whether a type would be tidier but whether it removes a way to be wrong. The
first four rows each name a specific wrongness the type makes unrepresentable.
Where no row matches, nothing is being prevented, and the primitive is what the
next reader already understands.

## SHOULD — Is inheritance right

POL-0037 · CG I.25, CG C.35, CG C.82, CG C.128, CG C.129

Almost always no. Inheritance shares *implementation*, and implementation
sharing is not how variation is represented.

| Question | Answer |
|----------|--------|
| Is this a fixed set of alternatives? | Not inheritance. Closed-set variation (POL-0033) |
| Is it an open set of behaviours, injected by a caller? | An abstract interface with no data |
| Is it code reuse? | Not inheritance. Composition, or a free function (POL-0029) |
| Do I have at least two concrete cases in hand? | If not, write the function. Decide on the second |

Where a hierarchy is genuinely right, three rules travel with it: a polymorphic
base class has a public virtual destructor or a protected non-virtual one; a
virtual function specifies exactly one of `virtual`, `override`, `final`; and no
virtual function is called from a constructor or a destructor.

Inheritance answers two unrelated questions at once — what the values are and
where the code lives — and binds the answers together permanently. Once a
hierarchy exists, adding an alternative is easy and adding an operation touches
every class, which is the opposite of the trade a closed set of alternatives
wants. The compiler also stops helping: nothing reports that a derived class
failed to handle something, because from the language's view nothing is missing.

## NEVER — Never build a hierarchy to represent a fixed set of alternatives

POL-0044 · CG C.129

A base class with a virtual destructor and one derived class per alternative is
a v-table where a variant belongs.

```cpp
// Never: the alternatives are fixed, and this spends an allocation to say so
class Event { public: virtual ~Event() = default; };
class Connect : public Event { std::string endpoint_; };
class Send : public Event { std::size_t size_bytes_; };

// Instead: the set is closed, so the compiler can check it is covered
using Event = std::variant<Connect, Send, Close>;
```

Inherit only for an open set of behaviours injected by a caller, behind an
interface that carries no data. POL-0037 is the test.

Three costs arrive together and none of them is visible at the declaration. Every
value becomes a heap allocation and a pointer chase, which is a performance
decision made by a type choice. Handling moves into virtual functions, so adding
an operation touches every class rather than one function. Most of all, the
compiler stops being able to report a missing case: adding a fourth derived class
is well-formed everywhere, including at the sites that needed to know.

## SHOULD — A distinct type for a dimensioned scalar is a named escape, not the default

POL-0038

A dimensioned value is a primitive with a unit-suffixed name (POL-0017). Wrapping
it in a distinct type is permitted under two conditions, both required:

- two units of the same underlying type are genuinely confusable at a boundary,
  **and**
- arithmetic does not flow through the type.

Where the value is carried rather than computed, the wrapper costs one
conversion at each end and removes a class of transposition. Where the value is
computed, it costs an operator for every arithmetic form the code uses.

```cpp
const double budget_ms = std::max(1.0, (deadline_ms - elapsed_ms) * 0.5);      // clear
const Millis budget = std::max(Millis{1.0}, (deadline - elapsed) * Millis{0.5});  // worse
```

A type that supports the full arithmetic of a domain correctly is a units
library, which is real infrastructure with real cost. A partial one produces
ceremony without safety: every operation it does not define is an operation the
author writes around, usually by unwrapping, which is where the safety went.

Unit suffixes plus params structs (POL-0023) already close the transposition
hole that motivates wrapping, at a fraction of the cost. The escape exists for
the case they do not cover, which is a boundary that hands over a bare scalar.

## SHOULD — Constraint-free data stays an aggregate `struct`

POL-0042 · CG C.2

Where the members can vary independently, the type is a `struct` with public
members and default member initializers. No constructor, no accessors, no
`private`.

```cpp
struct Extent {
    double width_px = 0.0;
    double height_px = 0.0;
};
```

The test is whether some combination of member values must never exist. A
coordinate pair, a colour triple, and a configuration bag of independent fields
all fail that test, so all three stay aggregates. POL-0015 is the rule; this is
its escape, and the escape is where most data types land.

Accessors that return a member and a constructor that assigns its arguments
protect nothing. They add a file's worth of code between the reader and the
data, and they cost the aggregate initialization that would otherwise make a
construction site self-describing (POL-0023). Encapsulation is bought to protect
an invariant, so where there is no invariant the purchase is all cost.

## MUST — Every enumeration is an `enum class`

POL-0103 · CG Enum.1, CG Enum.3

```cpp
// Never. Converts to int, so it compares equal to an unrelated enumeration.
enum CompactMode { Full, Incremental };

// Right.
enum class CompactMode { Full, Incremental };
```

An unscoped `enum` is permitted only to match a C API, for the reason POL-0046
permits a pointer-and-length pair at the same boundary: the foreign declaration
dictates the shape.

A macro or an integer constant where an enumeration belongs is the same defect
with less syntax. Both give up the distinct type, and with it the exhaustive
dispatch POL-0033 depends on.

An unscoped enumerator converts implicitly to `int`, so it can be passed where
a number is expected, compared against a different enumeration, and used in
arithmetic, all without a diagnostic. The enumeration then documents a closed
set that the type system is not enforcing, which is the gap POL-0043 names for
strings. `enum class` makes the set closed in the compiler rather than in the
reader's memory (POL-0008).

## SHOULD — An underlying type or an explicit enumerator value appears only when it is the contract

POL-0104 · CG Enum.7, CG Enum.8

```cpp
// Prefer. Nothing is claimed about representation.
enum class CompactMode { Full, Incremental };

// State both when the numbers cross a boundary and must not move.
enum class WireOpcode : std::uint8_t { Rapid = 0x01, Cut = 0x02, Dwell = 0x03 };
```

The contract cases are serialization, an FFI crossing (POL-0063), and a fixed
width a device or protocol requires. Absent one of those, the default
underlying type is correct and no enumerator carries a number.

A stated underlying type reads as a claim that the representation matters, and
a reader who finds one will preserve it through changes that did not need it.
Explicit values invite a gap or a duplicate, and a duplicate is the worse
failure: two enumerators that compare equal make a `switch` over them
unreachable in one arm, which defeats the exhaustiveness POL-0033 relies on
without producing a diagnostic.
