# Review Notes

This file is a durable review log for findings that are useful but are not yet
ready to become policy, standard, exemplar, or implementation changes.

Do not preserve conversation transcripts here. Preserve the engineering result:
what was reviewed, what the corpus currently does, where it is strong or weak,
and what follow-up should be considered.

## Entry format

Each review entry should use this shape:

```text
## YYYY-MM-DD — Short topic

### Scope
What was reviewed and what question prompted the review.

### Current guidance
What the repository already says or demonstrates.

### Assessment
How well the current corpus handles the problem, including important technical
nuance or corrections.

### Gaps
What cases are not currently constrained or demonstrated well enough.

### Recommended follow-up
Concrete changes worth considering. These are review notes, not automatically
approved changes.
```

---

## 2026-08-25 — Return value optimization and copy elision guidance

### Scope

Review the current policy and exemplar corpus for guidance around return value
optimization (RVO), named return value optimization (NRVO), copy elision, and
implementation patterns that preserve those optimizations.

The question was not merely whether the corpus mentions RVO, but whether its
current guidance is strong enough to steer generated C++ toward good return
shapes across a wide variety of implementations.

### Current guidance

The corpus already has a good foundation.

`docs/policies/POL-0049-no-rvalue-reference-return.md` gives the clearest RVO
rule. It says to return by value, let the compiler elide the copy, and never
write `return std::move(local)`. That is an important and correct constraint.
The policy also warns against returning `T&&` from a local object.

`docs/policies/POL-0037-output-is-returned.md` strongly prefers return values over
out-parameters and recommends returning a named struct for multiple outputs.
That naturally pushes implementations toward value-returning shapes where copy
elision can work.

`docs/policies/POL-0051-no-const-value-return.md` prevents another related
pessimization by forbidding `const T` as a by-value return type. The policy notes
that `const` on a value return can interfere with moving from the result and
silently turn moves into copies.

The C++17 convention material explicitly recognizes guaranteed copy elision and
uses that as part of the justification for returning values directly.

The exemplars also contain good direct-return shapes. For example,
`EXM-0001-value-type/core/temperature.cpp` returns `Temperature{celsius}`
directly from `Temperature::try_from()` rather than manufacturing a named local
that exists only to be returned.

Taken together, the corpus currently teaches several good instincts:

- return results by value;
- do not replace return values with output parameters merely to avoid copies;
- do not write `return std::move(local)`;
- do not return `const T` by value;
- construct and return values directly when that is the natural implementation.

### Assessment

The general behavior is good, but the RVO/NRVO guidance is not yet deep enough
to constrain a wide range of implementation shapes reliably.

The most important technical nuance is that the current wording in POL-0049 is
a little too strong for a named local:

```cpp
Toolpath build() {
    Toolpath path = assemble();
    return path;
}
```

This is an NRVO candidate. Compilers normally elide the move or copy, but NRVO
is permitted rather than universally guaranteed by the language.

That should be distinguished from the C++17 guaranteed copy-elision case:

```cpp
Toolpath build() {
    return Toolpath{/* ... */};
}
```

Here the returned object is constructed directly as the function result. There
is no intermediate `Toolpath` object that must later be moved or copied.

For a named local, if NRVO does not occur, normal return semantics can still
allow a move rather than a copy. That is another reason not to add
`std::move(local)` manually just to "help" the compiler.

The existing policy is therefore directionally correct, but it currently blurs
an important distinction:

- direct prvalue return: guaranteed copy elision in C++17 and later;
- named local return: NRVO opportunity, normally optimized but not the same
  language guarantee.

### Gaps

The current corpus appears not to give explicit guidance for several common
return shapes that determine whether NRVO remains available.

For example:

```cpp
T make() {
    return T{};
}
```

This is the clearest direct-construction shape.

```cpp
T make() {
    T result;
    // build result
    return result;
}
```

This is a conventional NRVO candidate and is generally a good shape when the
object must be assembled over several statements.

But more complicated control flow introduces cases the current guidance does not
really discuss:

```cpp
T make(bool choose_a) {
    T a;
    T b;

    if (choose_a) {
        return a;
    }
    return b;
}
```

Multiple distinct named return objects can prevent the implementation from
having the simple one-object NRVO shape.

By contrast, a function that builds one named result and returns that same
object along its return paths is much more naturally NRVO-friendly:

```cpp
T make(bool condition) {
    T result;

    if (condition) {
        // modify result
        return result;
    }

    // modify the same result
    return result;
}
```

Another good shape is to return prvalues directly from each branch when there is
no reason to maintain a common mutable result object:

```cpp
T make(bool condition) {
    if (condition) {
        return T{/* first form */};
    }
    return T{/* second form */};
}
```

The current corpus would probably generate many of these correctly because of
general C++ model knowledge, but it does not yet strongly constrain the model to
recognize and preserve these shapes because the policy/exemplar material does
not spell them out.

That is the main weakness: the corpus prevents the classic obvious mistakes, but
it does not yet teach implementation structure around copy-elision eligibility.

### Recommended follow-up

Add one compact policy specifically about preserving copy elision in
value-returning functions. It should not become a long RVO tutorial. It should
constrain implementation shape.

A useful rule would be approximately:

> Structure value-returning functions to preserve copy elision. Prefer direct
> construction of the returned value. When construction requires a named local,
> use one return object where practical and return it by name. Never add
> `std::move` merely to "help" the return.

The policy should demonstrate at least these four forms:

```cpp
// Best when practical: direct construction.
return Result{/* ... */};

// Good: one named result, eligible for NRVO.
Result result;
// build result
return result;

// Good: direct prvalues from different branches.
if (condition) {
    return Result{/* ... */};
}
return Result{/* ... */};

// Avoid when practical: several competing named return objects.
Result a;
Result b;
return condition ? a : b;
```

POL-0049 should also be tightened so it does not describe named-local NRVO as if
it were the same guarantee as C++17 prvalue copy elision.

An exemplar may also be worthwhile if there is a natural situation that builds a
non-trivial result over several statements. The exemplar should show both the
preferred direct-return form and the one-named-result NRVO form, without turning
the exemplar into compiler trivia.

### Overall conclusion

Current state: good general return-value behavior, incomplete optimization
shape guidance.

An LLM following the corpus is unlikely to make the classic
`return std::move(result)` mistake and is generally encouraged to return values
cleanly. However, across a broad set of RVO/NRVO examples, some correct behavior
would still depend on the model's general C++ knowledge rather than on explicit
constraints supplied by this repository.

That makes this a good candidate for a small, focused policy improvement rather
than a large new subsystem of guidance.
