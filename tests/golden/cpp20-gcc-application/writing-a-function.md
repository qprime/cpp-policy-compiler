cpp20-gcc-application › Writing a function

Read when: writing a signature or body — parameters, decomposition, duplication, templates, `auto`.

## MUST — Interfaces do not admit silent reordering

POL-0016 · CG I.23, CG I.24

No two adjacent parameters may be interchangeable: swappable by a caller,
changing what the call means, and drawing no complaint from the compiler. Keep
argument counts low.

Two triggers, either one sufficient:

- more than four parameters, regardless of their types
- two adjacent parameters of the same type, regardless of the count

Two routes satisfy the rule, and only one is required. Name the parameters, by
moving them into a params struct (POL-0023). Or make a transposition
ill-formed, by giving the confusable parameters distinct types (POL-0038 bounds
when that is worth its cost).

The escape is a genuinely conventional mathematical order that a reader would
be surprised to see disturbed: `lerp(a, b, t)`, `clamp(v, lo, hi)`,
`atan2(y, x)`. A struct does not improve these.

The defect is not the argument count. It is that the compiler cannot tell a
correct call from a transposed one, so the mistake survives compilation, review,
and any test whose inputs happen to be symmetric. Argument order is decided at
each call site and re-decided at every site added later, which makes the number
of chances to get it wrong grow with the number of callers rather than staying
fixed at one.

## NEVER — Never silence an unused parameter with a void cast

POL-0054

`(void)param;` marks a parameter that should not exist. On a leaf function,
delete the parameter and the call sites that pass it.

Allowed where the signature is mandated and cannot be changed: a virtual
override, an interface implementation, a callback registered with a foreign API.
There the unnamed-parameter form says the same thing without a statement:

```cpp
void on_event(const Event&, int /*retry_count*/) override;
```

An unused parameter is an interface claiming to need something it does not, and
every caller pays by computing a value that is discarded. The cast makes the
warning go away and leaves the claim standing, so the next reader supplies the
argument carefully and the one after that adds a second unused parameter by the
same reasoning. Deleting it is what makes the signature match what the function
does, which is the only version of the signature that stays true.

## THIS WAY — Params struct

POL-0023 · CG I.23, CG I.24, CG F.21

C++ has no keyword arguments, so a struct with designated initializers is how a
call site names what it is passing.

```cpp
// Wrong. Four adjacent doubles; every ordering compiles.
Result compact(const Store& store, double load_factor, double slack_ratio,
               double min_fill, double max_growth, CompactMode mode);

compact(store, 0.75, 0.10, 0.50, 2.0, CompactMode::Incremental);
//             ^^^^^^^^^^^^^^^^^^^^^ transpose any pair; still compiles
```

```cpp
// Right. Named fields at the construction site; no ordering to get wrong.
struct CompactParams {
    double load_factor;
    double slack_ratio;
    double min_fill;
    double max_growth;
    CompactMode mode = CompactMode::Full;
};

Result compact(const Store& store, const CompactParams& params);

compact(store, CompactParams{
    .load_factor = 0.75,
    .slack_ratio = 0.10,
    .min_fill = 0.50,
    .max_growth = 2.0,
    .mode = CompactMode::Incremental,
});
```

Designated initializers are C++20. On earlier standards the struct is still the
right shape: the fields are assigned to a named local before the call, or a
small builder produces it.

The same reasoning applies on the way out. A function with several outputs
returns a struct rather than taking out-parameters.

POL-0016 is the rule this satisfies, and it names the alternative route:
distinct types, which make a transposition ill-formed rather than merely
visible. Either is sufficient and neither requires the other.

A struct moves the parameter names from the declaration, where the caller cannot
see them, to the call, where the caller writes them. That converts an ordering
mistake from something the compiler accepts into something the author has to
type wrong on purpose. It also gives new parameters a place to arrive that does
not disturb existing call sites, so the interface can grow without a round of
edits that each risk the same transposition.

## NEVER — Never keep two functions that share most of their bodies

POL-0056

Two functions sharing more than half their bodies drift. A fix applied to one is
forgotten in the other, and nothing links them.

```cpp
// Never
Result compact_full(const Store& store, double min_fill);
Result compact_incremental(const Store& store, double min_fill);   // 40 of 50 lines identical

// Instead: one function, and the difference is a named field
Result compact(const Store& store, const CompactParams& params);   // params.mode
```

The test is whether a future change would have to be made in both places.
Accidental similarity that would not co-evolve stays separate, and merging it
produces a parameter that means nothing.

Duplication is cheap to create and its cost is entirely deferred. The two bodies
are identical on the day they are written, which is the only day anybody
compares them; from then on each is edited by whoever is working on its caller,
without cause to look at the other. The divergence is silent because both
compile and both pass their own tests, and it is found when two callers that
should agree do not.

## THIS WAY — Free function by default

POL-0029 · CG C.4, CG C.5

A function is a member only if it needs direct access to the representation.
Everything else is a free function in the same namespace.

```cpp
class SortedKeys { /* only what needs the representation */ };

// same namespace, not members — these need only the public interface
std::optional<Key> lower_bound(const SortedKeys& keys, const Key& target);
std::size_t count_in_range(const SortedKeys& keys, const Key& lo, const Key& hi);
SortedKeys merge(const SortedKeys& a, const SortedKeys& b);
```

The test is mechanical: write the function against the public interface first,
and make it a member only when that fails.

A type's interface should be as small as its invariant requires, because every
member is code that could break the invariant and therefore code that has to be
read before the type can be trusted. A free function cannot corrupt what it
cannot reach, so a defect in one is a defect in one place. The arrangement also
lets operations be added without touching the type, which means the set of
things that can be done with a value grows without the set of things that must
be audited growing with it.

## THIS WAY — Named operation

POL-0030 · CG F.1, CG F.2, CG F.3, CG F.8, CG F.56

A long function is usually several operations that have not been named. The
signal is not line count. It is whether the block can be named.

If a comment would explain a block, that block is a function and the comment is
its name.

```cpp
// Instead of one long compact() with four implicit phases:
std::vector<Segment> collect_live_segments(const Store& store);
std::optional<Segment> find_reclaim_candidate(const std::vector<Segment>& segments,
                                              double min_fill);
void emit_relocation(Journal& journal, const Segment& from, const Segment& to);
```

Prefer pure functions: same input, same output, no side effects. Those are the
ones testable in isolation and readable without their context. Avoid
unnecessary condition nesting; return early.

Decomposition is not the goal, and splitting a function that cannot be named
produces `compact_part_two`, which is worse than the original. The name is the
deliverable.

A named operation can be understood from its declaration, so the reader learns
what the code does without simulating it. An unnamed block can only be
understood by executing it mentally, and that reconstruction is where wrong
assumptions enter: the block shows what the code does and never what it was
required to do. Naming also fixes the boundary, which is what lets one phase be
replaced without re-reading the three around it.

## SHOULD — How to pass a parameter

POL-0035 · CG F.15, CG F.16, CG F.17, CG F.18, CG F.20, CG F.21, CG F.24, CG F.43, CG F.60, CG Con.3, CG I.13

| Pass by | When |
|---------|------|
| Value | Small and cheap to copy; or the callee modifies its own copy; or the callee moves from it |
| `const T&` | A larger type the callee only reads |
| `T&` | In-out. Rare — prefer returning a value |
| `T*` | Null is a meaningful value |
| `T&&` | The callee moves from it and the caller knows |
| Sequence view | A read-only or write-through sequence, spelled per the declared standard |
| Return by value | Output. Always preferred to an out-parameter |

Return a struct for multiple outputs. Never return a reference or a pointer to a
local.

The sequence view and the non-owning string parameter are the two rows whose
spelling moves with the standard:

| | C++11 | C++17 | C++20 |
|---|-------|-------|-------|
| Sequence | Iterator pair, or `const std::vector<T>&` when the caller genuinely owns a vector | same | `std::span<const T>` to read, `std::span<T>` to write |
| Non-owning string | `const std::string&` | `std::string_view` | `std::string_view` |

A `(const T*, size_t)` pair is permitted only at an `extern "C"` boundary, and it
is converted on entry (POL-0046). A non-owning view is never stored as a member
in any standard (POL-0047).

Passing is the one decision in a signature that every call site pays and none
can change. Getting it wrong is rarely a defect and always a cost: a large type
by value copies at every call, an out-parameter forces a default-constructed
local before every call, and a reference where a value belongs adds a lifetime
question to a function that had none. The table exists so the choice is made
from what the callee does rather than from what reads well in the declaration.

## NEVER — Never pass a sequence as a pointer and a length

POL-0046 · CG I.13

`(const T* data, std::size_t length)` puts the lifetime contract in a comment
and the bounds check on every caller. The two parameters are also adjacent and
independently wrong, so a stale length compiles.

```cpp
// Never: nothing ties the length to the pointer, and nothing ties either to a lifetime
Digest checksum(const std::uint8_t* data, std::size_t length);

// Instead: the sequence type carries its own bounds — POL-0035 per declared standard
Digest checksum(std::span<const std::uint8_t> bytes);
```

At an `extern "C"` boundary the foreign signature dictates the pair. Convert on
entry and never touch the raw pointer again.

```cpp
extern "C" int checksum_c(const std::uint8_t* data, std::size_t length) {
    const std::span<const std::uint8_t> bytes(data, length);
    // body uses bytes only
}
```

The pair is two facts that must agree, held by a language that will not check
that they do. Every caller re-derives the length, and a caller that re-derives it
from a stale variable produces an out-of-bounds read that is undefined rather
than diagnosed (POL-0019). Converting at the seam confines the disagreement to
one line, which is also the one line where the foreign contract is actually
known.

## NEVER — Never store a non-owning view as a member

POL-0047

A view refers to data it does not own — `std::span` or `std::string_view` where
the declared standard has them, an iterator pair or a bare pointer earlier.
Stored as a member, it ties the object's validity to data the object does not
control.

```cpp
// Never: the object outlives whatever the caller passed, and nothing says so
class Parser {
 public:
    explicit Parser(std::string_view text) : text_(text) {}
 private:
    std::string_view text_;
};

// Instead: own it if the object retains it
class Parser {
 public:
    explicit Parser(std::string text) : text_(std::move(text)) {}
 private:
    std::string text_;
};
```

Take a view as a parameter where the function needs the data only for the
duration of the call. Store an owning member where the object retains it. The
choice is decided by lifetime, not by the cost of the copy.

A stored view is a use-after-free waiting for a caller to go out of scope first,
and the construction site is where it looks correct. The defect surfaces
somewhere else, at a time determined by the caller's control flow, and it
surfaces as garbage data rather than as a fault, because the memory is usually
still mapped. Nothing in the class can detect it: the view has no way to know
whether what it points at is still there.

## SHOULD — Concrete types over templates

POL-0040 · CG T.10, CG T.11, CG T.120

Write the concrete type. Templatize on one of two triggers: a third concrete
caller forces it, or the alternative is a runtime-typed interface that loses
type checking.

A template parameter carries its constraint, spelled per the declared standard:

| C++11 | C++17 | C++20 |
|-------|-------|-------|
| `static_assert` in the body stating the requirement; SFINAE only where unavoidable | `if constexpr` and `static_assert` | A concept, or a `requires` clause |

On C++20 an unconstrained template parameter is incomplete. On earlier standards
a `static_assert` carries the same information to the reader and produces a
diagnostic at the right place; the concept is better because the compiler
enforces it at the call rather than at the instantiation.

Two callers are not a generalization, they are two callers. Generalizing from
two produces a parameterization shaped by a coincidence, and the third caller
then either fits by accident or forces the abstraction to be redone with three
callers already depending on it. Waiting costs one duplicated function and buys
the information that says which axis actually varies.

## NEVER — Never templatize for two callers

POL-0052 · CG T.10, CG T.120

A function with two concrete callers is not generic. It is two callers.

```cpp
// Never: the parameter is a coincidence of the two call sites
template <typename Container>
std::size_t total_size(const Container& c);

// Instead: write what the callers need; generalize on the third
std::size_t total_size(const std::vector<Entry>& entries);
```

Templatize on a third concrete caller, or where the alternative is a
runtime-typed interface that loses checking (POL-0040). On C++20 the parameter
carries a concept; earlier it carries a `static_assert`.

Generalizing from two examples produces an abstraction shaped by whatever those
two happened to share, which is usually not the axis that varies. Two callers do
not distinguish a real axis from a coincidence, so the third caller either fits
by luck or forces the parameterization to be redone with dependants already
attached. Waiting costs one duplicated function, which is cheap and visible; the
wrong axis costs a rewrite and is neither.

## NEVER — Never use `auto` where the type is the load-bearing fact

POL-0050 · CG ES.11

`auto` removes redundant repetition of a type name. It is not a default, and
where the type is what the reader needs to know, it removes the answer.

```cpp
auto it = entries.begin();               // fine — the type is noise
auto store = std::make_unique<Store>();  // fine — the type is on the right
auto result = compact(store, params);    // not fine — is this a Result, an optional, a bool?
```

The test is whether the right-hand side already spells the type, or the type is
unspellable. Where neither holds, write the type.

Removing a type name removes the one place a reader can check that a call
returns what the next line assumes. That check matters most exactly where the
name was omitted, because a returned optional and a returned value read
identically at the call and differ at every use after it. `auto` in that position
also survives a change to the callee's return type without a diagnostic, so the
code keeps compiling and starts meaning something else.

## MUST — A lambda names every capture; `[=]` and `[&]` are not written

POL-0114 · CG F.54

```cpp
// Never. What state does this carry? The list is the only place that says.
auto ready = [&] { return count >= limit && !cancelled; };

// Right.
auto ready = [&count, &limit, &cancelled] { return count >= limit && !cancelled; };
```

`[this]` counts as a default: it captures the whole object, so a lambda written
inside a member function reaches every member without naming one. Capture the
members it uses, by value.

The capture list is the only part of a lambda with lifetime consequences, and a
default capture hides exactly that. `[&]` binds whatever the body happens to
name, so adding one identifier to the body silently extends what the lambda
borrows, and nothing in the diff shows a lifetime changed. An explicit list
makes the ownership question answerable from the declaration, which is what
POL-0003 asks of every other construct.

## MUST — A lambda that outlives the current scope captures by value

POL-0115 · CG F.52, CG F.53

```cpp
// Never. handler_ outlives this function; label_ is a dangling reference.
void Panel::install() {
    const std::string label_ = title();
    handler_ = [&label_] { log(label_); };
}

// Right. The lambda owns what it needs.
void Panel::install() {
    handler_ = [label = title()] { log(label); };
}

// Right. Runs and dies inside the call; borrowing is safe and avoids a copy.
std::ranges::sort(tools, [&required_mm](const Tool& a, const Tool& b) {
    return a.fit(required_mm) < b.fit(required_mm);
});
```

Stored in a member, returned, queued, or handed to another thread all count as
outliving. By-reference capture is permitted only where the lambda provably
runs and dies within the current scope, which is the algorithm-comparator case
above.

A by-reference capture is a non-owning view with the lifetime rules of one
(POL-0047), and it carries no diagnostic when it escapes. The compiler accepts
a returned lambda holding a reference to a dead local exactly as readily as a
correct one, so the defect surfaces as corrupted data at call time rather than
as a build failure. Capturing by value converts the question from a lifetime
the reader has to trace into a copy the declaration states.

## SHOULD — A lambda is trivial glue at one call site; anything else is a named function

POL-0116 · CG F.11, CG F.50, CG T.40, CG T.141, CG C.170, CG ES.28

```cpp
// Prefer. One use, one line, reads better inline than as a jump to a name.
std::ranges::sort(moves, [](const Move& a, const Move& b) { return a.z < b.z; });

// Prefer a function. Two uses, and it wants a name to be understood.
bool is_finishing_pass(const Move& m);
```

A lambda also earns its place initializing a `const` value that needs several
statements to compute, which is the one case where the alternative is a
non-`const` variable assigned later (POL-0020).

Where a lambda would be overloaded on argument type, write one generic lambda
rather than a set.

A lambda buys locality, not brevity. It is justified when reading the body in
place beats jumping to a name, which is true for a comparator and false for
anything a reader would need to think about. Once it wants a name, wants a
comment, or acquires a second use, it is a function that has not been given its
name yet, and POL-0030 already says what to do about that.

See also: [POL-0017 — Dimensioned values carry their unit in the name](naming.md)
