cpp20-gcc-application › Building a class

Read when: writing a type's mechanics — constructors, invariants, special members, `noexcept`, wrapper types.

## MUST — Types with invariants establish them at construction

POL-0015 · CG C.2, CG C.40, CG C.41, CG C.42

No object exists in an invalid state. A type whose members can vary
independently is a `struct`. A type with a constraint across its members is a
`class` whose constructor enforces that constraint and throws when it cannot be
met.

The test is a question about the data, not about encapsulation: is there a
combination of member values that must never exist? If yes, the constructor is
the only way in. If no, the type is an aggregate and wrapping it buys nothing
(POL-0042).

There is no `init()` a caller must remember to call, and no partially
constructed state to observe. A constructor either produces a valid object or
does not return.

POL-0022 carries how such a type is built, including the non-throwing
`try_from` form for callers that want to test rather than catch.

An invariant that is not established at construction is established by every
consumer instead, and each consumer chooses its own fallback for the invalid
case. Two sites that disagree produce two behaviours for one input, and nothing
connects them, so the divergence is invisible until the outputs are compared.
The constructor answers the question once, at the one place the object comes
into existence.

## MUST — Rule of zero

POL-0021 · CG C.20, CG C.21, CG C.22, CG C.66

Declare no special member function unless you must. If you declare or `= delete`
any one of the copy constructor, copy assignment, move constructor, move
assignment, or destructor, then declare or `= delete` all five.

Move operations are `noexcept`. Comparison is written by hand and symmetric
before C++20; from C++20 it is `= default` on `operator==` and `operator<=>`
for ordering.

POL-0025 carries the shape a type takes when it genuinely must own a resource
directly.

Declaring a destructor suppresses implicit move generation, which silently turns
every move of the type into a copy. There is no diagnostic for that, no test
that fails, and no line of code that changed; the cost appears as a performance
regression whose cause is a declaration in a header. Declaring all five is what
makes the set of operations a single stated decision rather than four
consequences of one.

## NEVER — Never apply `noexcept` as a blanket

POL-0051 · CG E.12, CG C.66

`noexcept` is a claim about behaviour, not an annotation. Where the claim is
false the program calls `std::terminate`, with no unwinding and no handler.
"It is free" is wrong.

Write it where it is genuinely true and where it changes something:

- move constructor and move assignment (POL-0021)
- `swap`
- destructors, which are already `noexcept` by default
- functions doing pure arithmetic on built-in types

The blanket is attractive because the compiler accepts it everywhere and no test
fails. The claim is then checked at the one moment it matters, in production,
by terminating the process; a recoverable failure becomes an unrecoverable one
and the diagnostic that would have said why is exactly what was skipped. A
function marked `noexcept` also constrains every future edit to its body, and
nothing reminds the person making that edit that the constraint is there.

## THIS WAY — Value type with invariant

POL-0022 · CG C.2, CG C.8, CG C.41, CG C.42, CG C.45, CG C.46, CG C.49, CG Con.2

The type that carries a constraint makes the constructor the only way in, so no
consumer has to ask whether the constraint holds.

```cpp
class RetryPolicy {
 public:
    RetryPolicy(int max_attempts, double backoff_ms, double jitter_ratio);

    int max_attempts() const { return max_attempts_; }
    double backoff_ms() const { return backoff_ms_; }
    double jitter_ratio() const { return jitter_ratio_; }

 private:
    int max_attempts_;
    double backoff_ms_;
    double jitter_ratio_;
};

RetryPolicy::RetryPolicy(int max_attempts, double backoff_ms, double jitter_ratio)
    : max_attempts_(max_attempts),
      backoff_ms_(backoff_ms),
      jitter_ratio_(jitter_ratio) {
    if (max_attempts <= 0) {
        throw std::invalid_argument("RetryPolicy: max_attempts must be > 0, got " +
                                    std::to_string(max_attempts));
    }
    if (jitter_ratio < 0.0 || jitter_ratio > 1.0) {
        throw std::invalid_argument("RetryPolicy: jitter_ratio must be in [0, 1], got " +
                                    std::to_string(jitter_ratio));
    }
}
```

Six rules travel with the shape:

- Validate in the constructor, never in an `init()` the caller must remember.
- Throw when construction cannot produce a valid object; the message is
  POL-0011.
- Members are `private` and accessors are `const`.
- Initialize in the member-init list; do not assign in the body.
- A single-argument constructor is `explicit`.
- Do not write a default constructor that only zeroes members. Use default
  member initializers.

Where a caller wants to test rather than catch, add a static `try_from`
alongside. It delegates to the constructor and does not restate the validation;
its return type is the optional mechanism for the declared standard (POL-0009).

```cpp
static std::optional<RetryPolicy> try_from(int max_attempts, double backoff_ms,
                                           double jitter_ratio);
```

Without the invariant, every consumer defends itself, and each one picks its own
value for the invalid case. Two such sites produce two behaviours for one input
and nothing links them, so the disagreement surfaces as an output difference
nobody can trace to a declaration. With the invariant both defences delete, and
the question of what an invalid value means is answered once, where the object
is created.

## THIS WAY — A type that owns a resource directly owns nothing else

POL-0025 · CG C.20, CG C.31, CG P.11

A type built out of values and standard containers declares no special member
functions, because the generated ones are correct.

```cpp
class Journal {
 public:
    explicit Journal(std::vector<Entry> entries);
    // no destructor, no copy, no move — all correct by default

 private:
    std::vector<Entry> entries_;
};
```

A resource with no RAII wrapper — an OS handle, a C library object, a mapping —
gets a type of its own that does nothing but own it. That type writes the five
special members (POL-0021); everything else composes it and goes back to
declaring none.

```cpp
class FileHandle {          // owns the descriptor and nothing else
 public:
    explicit FileHandle(const std::string& path);
    ~FileHandle();
    FileHandle(FileHandle&&) noexcept;
    FileHandle& operator=(FileHandle&&) noexcept;
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    int fd() const { return fd_; }

 private:
    int fd_;
};
```

Hand-written special members are where lifetime bugs live, so the pattern is
arranged to need as few of them as possible. Confining them to a type with one
member means the copy, the move, and the destructor each have one thing to get
right, and they are reviewable in isolation from whatever composes them. A type
that owns a handle *and* holds application state has to get both right in every
one of the five, and gets rewritten whenever the application state changes.

## THIS WAY — Wrapper type for preconditions

POL-0027 · CG I.5

A function with a *structural* precondition — sorted, non-empty, acyclic,
normalized, deduplicated — takes a type that proves it. The check runs once, at
the boundary, instead of inside every algorithm that wants to assume it.

```cpp
class SortedKeys {
 public:
    static std::optional<SortedKeys> try_from(std::vector<Key> keys);
    const std::vector<Key>& keys() const { return keys_; }

 private:
    explicit SortedKeys(std::vector<Key> keys);
    std::vector<Key> keys_;
};

std::optional<Key> lower_bound(const SortedKeys& keys, const Key& target);
```

`lower_bound`'s signature *proves* its precondition. An unsorted vector cannot
reach it without passing through `try_from`, so the function neither re-checks
nor trusts a comment.

Two bounds on the pattern:

- **Scalar preconditions get no wrapper.** A positive count belongs on the type
  that owns the count field (POL-0022). Reserve wrappers for structure.
- **Repeated `assert`s are a missing wrapper.** When a function asserts the
  same precondition its callers also assert, the precondition wants to be a
  type.

This is how "state preconditions" is satisfied without taking a library
dependency for two macros: the precondition is not stated, it is made
unrepresentable. Where structure does not admit a wrapper, the precondition is
`assert`ed and documented instead.

A stated precondition is checked by whoever remembers it, which is everyone at
first and nobody after the third caller. A precondition in the parameter type
is checked by the compiler at every call, including the calls written later by
someone who never read the function. That converts an open-ended obligation on
callers into one conversion site whose failure is visible.

## MUST — A class with a virtual function states its destructor and suppresses copying

POL-0120 · CG C.67, CG C.127, CG C.130, CG C.133, CG NR.7

```cpp
class Exporter {
 public:
    virtual ~Exporter() = default;
    Exporter(const Exporter&) = delete;
    Exporter& operator=(const Exporter&) = delete;
    Exporter(Exporter&&) = delete;
    Exporter& operator=(Exporter&&) = delete;

    virtual void write(std::span<const Move> moves) = 0;

 protected:
    Exporter() = default;
};
```

The destructor is public and `virtual` where the base is deleted through, and
protected and non-`virtual` where it is not. Copy and move are deleted, because
copying a base subobject out of a derived object is the slicing POL-0121
forbids; a hierarchy that needs copying provides a `virtual clone` returning
`std::unique_ptr`.

Data members are `private`. `protected` data is an interface with no
invariant — every derived class can break what the base established, and the
base has no way to state what it required.

Deleting through a base with a non-`virtual` destructor is undefined behaviour,
and it is undefined silently: the derived destructor does not run, so the
program leaks or corrupts rather than crashing where the mistake is. Stating
the destructor either way makes the decision visible at the point a reader asks
whether this type is meant to be deleted polymorphically.

This applies only once POL-0037 has established that a hierarchy is right at
all. Variation among a fixed set of alternatives is `std::variant` (POL-0044).

## NEVER — Never copy a polymorphic object by value, and never index one through a base pointer

POL-0121 · CG ES.63, CG C.145, CG C.152, CG T.81

```cpp
// Never. Copies the Exporter subobject; the derived half is discarded.
void emit(Exporter e);

// Never. Base and derived have different sizes; the arithmetic is wrong.
GcodeExporter items[4];
Exporter* p = items;
p[2].write(moves);

// Right. Access through a reference or a pointer, hold ownership as unique_ptr.
void emit(const Exporter& e);
std::vector<std::unique_ptr<Exporter>> exporters;
```

A container of polymorphic objects holds `std::unique_ptr` (POL-0014), never
values, and never a raw array.

Slicing compiles without a diagnostic and produces an object of the base type
holding the base's data, so the virtual call dispatches to the base
implementation and the derived behaviour is simply absent. Nothing reports it;
the program runs and does the wrong thing, which is the failure POL-0002 ranks
worst.

Array indexing through a base pointer is the same defect in pointer arithmetic:
the subscript scales by the base's size while the objects are the derived size,
so every element past the first addresses the middle of an object.

## MUST — An operator is defined only for its conventional meaning

POL-0122 · CG C.160, CG C.162, CG C.163, CG C.167, CG C.166

```cpp
// Never. + does not mean "append a move to a plan".
Plan operator+(const Plan& p, const Move& m);

// Right. The operation has a name.
Plan with_move(const Plan& p, const Move& m);

// Right. Arithmetic on a dimensioned value is what + means.
constexpr Millis operator+(Millis a, Millis b) { return Millis{a.count() + b.count()}; }
```

Overload only across operations that are genuinely equivalent — the same
operation on different argument types. Two overloads of one operator that do
different things are two operations sharing a name, which is the case a name
exists to distinguish (POL-0006).

`operator&` is overloaded only as part of a smart pointer or reference system,
and `operator->` only on a type that stands in for a pointer.

An operator is a name whose meaning the reader already knows, which is the
entire value of using one. A `+` that appends, a `<<` that does anything but
stream or shift, an `operator bool` on a type that is not a truth value — each
spends the reader's existing knowledge to buy brevity, and the reader has no
way to discover the substitution except by opening the definition. A named
function costs the same keystrokes and states what it does (POL-0030).

## MUST — A symmetric operator is a free function in its type's namespace, and conversions are `explicit`

POL-0123 · CG C.161, CG C.164, CG C.165, CG C.168

```cpp
namespace proj::geom {

class Millis {
 public:
    explicit constexpr Millis(double count) : count_{count} {}
    explicit constexpr operator double() const { return count_; }
    constexpr double count() const { return count_; }
 private:
    double count_;
};

constexpr bool operator==(Millis a, Millis b) { return a.count() == b.count(); }

}
```

A symmetric operator is a free function so both operands convert alike; a member
`operator==` converts only its right-hand side, which makes `a == b` and `b == a`
behave differently. It lives in the same namespace as its type, so
argument-dependent lookup finds it without a `using` declaration.

A conversion operator is `explicit`, and a customization point is opted into
with a `using` declaration at the call site rather than by defining a function
in someone else's namespace.

An implicit conversion operator makes a type participate in overload resolutions
nobody wrote it for. The type then converts silently in a comparison, an
arithmetic expression, or an overload it was never meant to match, which is the
same defect POL-0038 avoids by making a distinct type a named escape rather than
a transparent one.

## MUST — When copy or move is written out, it takes the standard shape

POL-0125 · CG C.60, CG C.61, CG C.62, CG C.63, CG C.64, CG C.65

| Operation | Signature |
|-----------|-----------|
| Copy assignment | `T& operator=(const T&)`, non-`virtual` |
| Move assignment | `T& operator=(T&&) noexcept`, non-`virtual` |

A copy produces an independent object: mutating the copy must not be observable
through the original. A move leaves its source in a valid, destructible,
assignable state — empty is the usual choice, and the source is never left in a
state where the destructor is unsafe.

Both assignments are safe against self-assignment, including the move case,
which a naive release-then-take implementation gets wrong.

This is reached only when POL-0021 does not apply. Rule of zero is the default,
and a type that owns exactly one resource through a standard handle needs none
of this written out.

The shape is fixed because callers and the standard library depend on it. A
`virtual` assignment operator makes assignment through a base slice silently
(POL-0121), returning by value instead of `T&` breaks chained assignment, and a
move assignment that is not `noexcept` causes `std::vector` to copy rather than
move on reallocation — a performance change with no diagnostic.

## MUST — A value type behaves like `int`

POL-0126 · CG C.11, CG C.12, CG C.43, CG C.44, CG C.134

```cpp
class Millis {
 public:
    Millis() = default;
    explicit constexpr Millis(double count) : count_{count} {}
    constexpr double count() const { return count_; }
 private:
    double count_{0.0};
};
```

Copyable, movable, comparable, default-constructible to a meaningful empty or
zero, and free of surprises when placed in a container. The default constructor
is simple and does not throw.

No data member is `const` or a reference on a copyable or movable type. Either
one deletes assignment silently, so the type stops being assignable and every
container operation that needs assignment stops compiling, with an error that
points at the container rather than at the member.

Every non-`const` data member is `private`. Mixed access levels mean part of the
representation is an invariant and part is not, and no reader can tell which
without checking each one. A type whose members are genuinely all public and
constraint-free is an aggregate `struct` (POL-0042), not a class with some
members exposed.

Regularity is what lets a type be used without being studied. A value that
copies, compares, and sorts the way `int` does needs no documentation to be put
in a `std::vector` or a `std::map`, and every deviation is a special case
someone has to learn before they can use it (POL-0004).
