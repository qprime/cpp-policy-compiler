cpp20-gcc-application › Handling failure

Read when: choosing what happens when an operation cannot do what it was asked.

## MUST — Errors carry the four-part message

POL-0011

Every constructed message states four things. This holds for exceptions, result
payloads, log lines, and structured warnings alike.

1. **What failed.** The class, function, or subsystem.
2. **What field.** The specific parameter or invariant.
3. **What constraint.** The rule that was broken.
4. **Actual value.** What was received.

```cpp
throw std::invalid_argument("RetryPolicy: max_attempts must be > 0, got 0");
```

A message missing any part forces whoever reads it back to the source to
reconstruct the rest, and the reader is often a process that has no source in
front of it. `"invalid argument"` identifies nothing. `"max_attempts is
invalid"` omits the constraint and the value, which are the two parts that say
whether the caller or the callee is wrong. Naming the origin first is what lets
a message read far from where it was thrown still be placed.

## THIS WAY — Failure mechanism

POL-0031 · CG E.1, CG E.2, CG E.14, CG E.15, CG E.30, CG F.60, CG I.5, CG I.10

Pick by what the caller needs, not by what is convenient to write.

| Mode | Use when |
|------|----------|
| Optional | Absence is the only failure mode and there is nothing to explain (POL-0009) |
| Result type | Failure carries information the caller must act on |
| Exception | Genuinely exceptional: allocation failure, invariant violation, unrecoverable corruption |
| `assert` | "Cannot happen", because upstream validation already guarantees it. Sparingly; repeated asserts mean a missing wrapper type (POL-0027) |
| Silent partial output | **Never.** |

The result type is `std::expected<T, E>` from C++23. Earlier standards use a
project-local result type and migrate on the move to 23; they do not take a
third-party `expected` for it.

Exception types are purpose-designed, never built-in ones reused. Throw by
value, catch by reference, and use no exception specification other than
`noexcept`.

Where a module compiles without exceptions — a real-time target, a small binary,
some FFI hosts — one error-code convention is chosen for that module and stated
in its top-level header. The word doing the work is *one*: a module with two
conventions has neither.

The mechanism is part of the signature, so choosing it wrongly is a decision
every caller inherits and none can revise. An exception where a result belongs
forces every caller into a `try` block for an outcome that is ordinary; a result
where an exception belongs makes an unrecoverable state something a caller can
ignore by not reading the return. Choosing from what the caller must do is what
keeps the cost at the one site that knows.

## THIS WAY — Failure becomes less fatal moving outward

POL-0032

The layer a failure occurs in decides what happens to it. Parsers are strict;
orchestrators tolerate per-item failure and stay strict about safety.

| Layer | On failure |
|-------|-----------|
| FFI boundary | Translate into the host language's mechanism. Never let one cross unhandled (POL-0059). |
| Module public API | Return a result type for recoverable failure; throw only for invariant violations. |
| Internal helpers | Trust contracts. Input was validated upstream; `assert` cheaply where defensible. |
| Real-time loop | Record in a pre-allocated trace and continue. Never throw (POL-0076, POL-0077). |
| Real-time loop boundary | Inspect the accumulated trace and decide whether to halt. |

Read the table as a question about position, not severity. The same failing
operation gets a different treatment depending on which layer called it, and the
layer is what the author knows without looking anything up.

A uniform failure policy is wrong at both ends. Applied at the strictness of a
parser, an orchestrator aborts a whole run for one bad item; applied at the
tolerance of an orchestrator, a parser accepts malformed input and hands the
defect downstream where its origin is gone. Tying the treatment to the layer
puts the decision where the information about the caller's options actually is.

## SHOULD — Exceptions are permitted at module boundaries

POL-0039 · CG E.25, CG E.26, CG E.27

An exception is for a genuinely exceptional condition raised at a module
boundary: allocation failure, invariant violation, unrecoverable corruption. A
routine fallible operation returns a result type instead (POL-0031).

Three named escapes bound where exceptions may appear:

- **Forbidden in real-time loops.** Their timing is not deterministic
  (POL-0076).
- **Never cross an FFI boundary un-translated.** Translation happens exactly
  once, at the binding layer (POL-0059).
- **`-fno-exceptions` is permitted per module** when latency, binary size, or an
  FFI target justifies it, declared in that module's top-level header.

A module compiled without exceptions follows the exception-free discipline:
simulate RAII for resource management, fail fast where that is the right answer,
and use error codes systematically — one convention for the module, stated where
its header states the compilation mode.

This is narrower than the general position that exceptions are the error-handling
mechanism, and the narrowing is deliberate. That position assumes neither a
latency deadline nor a foreign-language seam, and both are present here. Where
neither applies, an exception at a module boundary is the right mechanism and
carries no apology.

## NEVER — Never catch to re-throw a different type at every layer

POL-0053 · CG E.3, CG E.17, CG E.18

Catching an exception in order to throw a different one, layer after layer,
produces noise that buries the one place handling actually happens.

```cpp
// Never: three layers of this, and the original site is gone by the top
try {
    return parse(text);
} catch (const ParseError& e) {
    throw StoreError(std::string("parse failed: ") + e.what());
}
```

Translate exactly once, at the FFI boundary, into the host language's mechanism
(POL-0059). Everywhere else, let the exception pass and let the layer that can
act on it catch it (POL-0032).

Exceptions as control flow are forbidden outright.

Each translation replaces a type the handler could have matched on with a string
the handler cannot, and discards the context the original carried. The `try`
blocks then have to exist at every layer, which means every layer's ordinary
path is written around a failure it does nothing about. What survives to the top
is a message assembled from prefixes, and no way to tell which layer originated
the failure or what the caller could have done differently.

## NEVER — Never ship a public function that returns `{}` because it is unimplemented

POL-0055

A function in a public header returning a default-constructed value is
indistinguishable from one that legitimately produced an empty result.

```cpp
// Never: the caller gets an empty result and no reason to doubt it
std::vector<Entry> load_entries(const Path& path) { return {}; }

// Instead, where a caller needs the symbol before the body exists
[[noreturn]] std::vector<Entry> load_entries(const Path& path);
// ... throws std::logic_error("not implemented: load_entries")
```

Deletion is the first answer. The throwing form exists for the case where a
caller must compile against the symbol first. An unimplemented function gets no
FFI binding.

The empty return is a silent wrong answer, which is the failure mode with no
downstream detection at all (POL-0002). Callers write their handling for the
empty case, tests are written that pass against it, and the stub acquires
dependants that will keep working when the real body lands and starts returning
data. Whoever implements it then discovers the interesting part was never the
body, it was the four callers who built on the empty result.

## MUST — No code that can throw runs while holding something nothing will release

POL-0163 · CG E.13, CG E.19

```cpp
// Never. If the second allocation throws, the first leaks.
void install(Widget* w) {
    Node* n = new Node(w);
    registry_.add(n);
}

// Right. Owned before anything else can fail.
void install(std::unique_ptr<Widget> w) {
    registry_.add(std::make_unique<Node>(std::move(w)));
}
```

Where the thing to release has no resource-owning type available — a C handle, a
registration that must be undone, a temporary state change — use a scope guard: a
small object whose destructor runs the cleanup, released explicitly on the
success path.

```cpp
auto guard = ScopeExit{[&] { ::freeaddrinfo(info); }};
```

This is POL-0127 stated as an invariant rather than a prohibition. A raw
allocation is one instance of holding something unowned; a file descriptor, a
lock taken by hand, and a half-finished registration are others, and all of them
leak on the same paths.

An exception makes every statement between acquisition and release into an exit
path, including ones nobody wrote. Ownership by a destructor covers all of them
at once, which is why POL-0003 makes it the default rather than a technique.

## MUST — `catch` clauses are ordered most-derived first, and catch by `const&`

POL-0164 · CG E.31

```cpp
// Never. The base clause matches everything; the second is unreachable.
try { load(path); }
catch (const std::exception& e) { report(e); }
catch (const std::filesystem::filesystem_error& e) { retry(e); }

// Right.
try { load(path); }
catch (const std::filesystem::filesystem_error& e) { retry(e); }
catch (const std::exception& e) { report(e); }
```

Catch by `const&`. Catching by value slices a derived exception down to the
caught type (POL-0121), so the handler loses exactly the information that
distinguished it.

`catch (...)` appears only where the frame must not propagate — the outermost
handler of a thread, or the binding layer translating to the host language
(POL-0059) — and it always rethrows or reports rather than discarding.

Clauses are tried in written order, not by best match, which is the opposite of
overload resolution and the reason this needs stating at all. A base-class
clause written first silently makes every later clause dead code, and most
compilers do not warn.
