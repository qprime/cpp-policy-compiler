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
