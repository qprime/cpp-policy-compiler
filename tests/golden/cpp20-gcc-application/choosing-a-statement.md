cpp20-gcc-application › Choosing a statement

Read when: shaping control flow — which loop, which selection, early returns, `switch` arms and fallthrough.

## SHOULD — Control flow takes the plainest statement that fits

POL-0117 · CG ES.70, CG ES.72, CG ES.73, CG ES.75, CG ES.77, CG ES.85, CG NR.2, CG NR.6

| Situation | Statement |
|-----------|-----------|
| Choosing among values of one variable | `switch` |
| An obvious loop variable | `for`, or range-`for` per POL-0099 |
| No obvious loop variable | `while` |
| A body that must run before the first test | Restructure; `do`-`while` is not written |

An early `return` is preferred to nesting, and there is no rule against several
of them. Cleanup rides on destructors (POL-0003), so no function needs a single
exit or a jump to a shared epilogue.

`break` and `continue` are permitted, sparingly, where they remove nesting the
reader would otherwise have to hold. An empty statement is written as `{}` on
its own line, never as a bare semicolon.

A `switch` over an enumeration is what makes an added enumerator a compile error
under POL-0033, which an `if`-chain over the same values will not do. The rest
of the table is uniformity: where two spellings are equally correct, taking the
common one costs nothing and removes a decision from every later edit
(POL-0004). A `do`-`while` inverts the reader's expectation that a loop tests
before it runs, which is why it is worth restructuring around rather than
spending attention on.

## NEVER — Never write `goto`

POL-0118 · CG ES.76

```cpp
// Never. The C idiom for cleanup, in a language that has destructors.
int load(const char* path) {
    FILE* f = std::fopen(path, "rb");
    if (!f) { goto fail; }
    if (!read_header(f)) { goto cleanup; }
    ...
cleanup:
    std::fclose(f);
fail:
    return -1;
}

// Right. The destructor is the cleanup path, and there is one exit per outcome.
std::expected<Header, LoadError> load(const std::filesystem::path& path) {
    auto file = FileHandle::open(path);
    if (!file) { return std::unexpected(LoadError::NotFound); }
    return read_header(*file);
}
```

Take an early `return` and a resource-owning type (POL-0117, POL-0025).

`goto` exists in generated C++ because the training corpus contains C, where it
is the only way to reach one cleanup block from several failure points. C++
removed the need: a destructor runs on every path out of a scope, including the
ones nobody wrote. What remains is a jump that makes the set of paths into a
block unbounded, so no reader can enumerate the states in which a label is
reached, and no compiler warning depends on it.

## MUST — A `switch` states every case and never falls through by accident

POL-0119 · CG ES.78, CG ES.79

```cpp
// Never. Is the missing break deliberate? Nothing says, and no warning fires.
switch (mode) {
    case CompactMode::Full: prepare();
    case CompactMode::Incremental: run(); break;
}

// Right. Deliberate fallthrough is marked; the rest break.
switch (mode) {
    case CompactMode::Full:
        prepare();
        [[fallthrough]];
    case CompactMode::Incremental:
        run();
        break;
}
```

A `switch` over an enumeration lists every enumerator and has no `default`.
`default` is for a genuinely open set — a value arriving from outside the
program — and there it handles the common case rather than silently absorbing
everything.

Omitting `default` is what makes `-Werror=switch` under POL-0089 report a new
enumerator as a build error, which is the mechanism POL-0033 relies on. A
`default` arm defeats it: the switch keeps compiling after the enumeration
grows, and the new case falls into whatever the default happened to do. Marked
fallthrough is the same argument at statement level — the compiler cannot
distinguish an intended fallthrough from a forgotten `break` unless the code
says which one it is.
