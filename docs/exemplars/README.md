# Exemplars

Whole compilable source, showing what a policy fragment and a standard entry cannot:
composition. Where the includes go, how a header relates to its implementation and
its test, how a name chosen under one entry reads beside a type built under another.

An exemplar cites the ids it demonstrates. It never restates the guidance behind
them, which is the same boundary the corpus holds against
[the coding standard](../policies/README.md#the-coding-standard-boundary): a second
copy of the guidance is a copy that drifts.

## On-disk format

One directory per exemplar, named `EXM-NNNN-<slug>/`, holding an `exemplar.md` and a
self-contained source tree beneath it.

```
docs/exemplars/EXM-0001-value-type/
    exemplar.md
    include/sampler/core/temperature.hpp
    core/temperature.cpp
    core/temperature_test.cpp
```

The tree is laid out as [STD-0003](../standard/STD-0003-directory-and-namespace-layout.md)
fixes it, with the exemplar directory standing in for the project root. Every include
path is written from that root, so an exemplar copied into a real project needs no
edits.

### Identity

`EXM-NNNN`, zero-padded, allocated highest-existing-plus-one in author order. Never
reused, never reassigned. The slug in the directory name is a human convenience;
frontmatter `id` is the citable thing.

### Frontmatter

| Key | Presence | Meaning |
|-----|----------|---------|
| `id` | required | `EXM-NNNN`. Matches the directory prefix, unique across the layer. |
| `demonstrates` | required | A list of `POL-NNNN` and `STD-NNNN` ids, never empty. Every entry resolves to an existing policy or standard entry, and never to an anti-pattern. |
| `applicability` | optional | Axis marks that constrain the exemplar out. Same axes and same value shape as a policy: `language_version`, `compiler`, `domain`. Absent entirely means universal. |

There is no `attribution`. An exemplar derives from the corpus rather than from
source material, and `demonstrates` is its whole provenance. The key is rejected
rather than ignored if it appears.

An anti-pattern is code not to write, so an exemplar demonstrating one would assert
the reverse of the truth. Principles stay legal, and a cited principle links to
`index.md`.

### Body

The H1 carries the statement. What follows is a reading order naming the files in
the order a reader should open them, one clause each. No prose rules and no restated
policy content.

The statement renders as an H2 in `exemplars.md`, so a heading in the body starts at
`###`. A body H2 would sit beside fourteen others of the same name, and a reader
navigating by heading would find `Reading order` as a peer of the situation it
belongs to.

## Applicability records an honest floor

Absence means universal, and universal reaches every language version the compiler
knows: `14`, `17`, `20`, `23`. An exemplar carries the floor of the facilities its
code actually uses, set once the code is written rather than assumed ahead of it.

| What the code uses | Mark |
|--------------------|------|
| Nothing above C++14 | none |
| `std::optional`, `std::variant`, structured bindings | `["17", "20", "23"]` |
| `std::jthread`, concepts, `std::span`, defaulted comparison, coroutines | `["20", "23"]` |

Each exemplar is written in the best form for a modern standard, and the mark records
what that cost. An exemplar contorted to reach C++14 demonstrates the wrong shape. A
projection at a language version below an exemplar's floor omits it, which is the
exclusion mechanism working rather than a gap.

## What a test may claim

A test asserts observable behaviour. A compile-time property is asserted by
`static_assert` at the definition site, not in a test file. A property that neither a
run nor a compile can establish is demonstrated by the shape of the code and is not
named as a test at all.

Naming a test for something a passing run does not establish teaches a model to write
tests that lie, which is worse than teaching it nothing. Instrumentation is admissible
where it is scoped honestly: a counting `operator new` establishes that one path did
not allocate on one input, and the test name says exactly that.

## The domain

Every exemplar inhabits one device-sampling domain, so a reader moving between them
carries the vocabulary rather than relearning it. Project name is `sampler`. Layers
are `core`, `device`, `wire`, and `ffi`. Tests are written in Catch2, as
[STD-0029](../standard/STD-0029-test-framework.md) fixes it.

### Canonical types

Three scalar value types are owned by [EXM-0001](EXM-0001-value-type/) and copied
verbatim, with their sources and their tests, wherever else they appear. An edit to
EXM-0001 requires a sweep of the copies, and because the copies are verbatim they are
comparable region by region.

| Type | Layer | Carries |
|------|-------|---------|
| `Temperature` | core | A celsius reading at or above absolute zero |
| `DeviceId` | core | A non-empty device identifier, ordered so it can key a container |
| `SampleInterval` | core | A strictly positive sampling period |

Compound types are never shared and never reused by name. Two exemplars that both
hold a decoded reading give it two names drawn from their own situations, because one
name covering two definitions is worse than two names. No exemplar includes another
exemplar's headers.

`Duration` is not used. `std::chrono::duration` exists, and an exemplar that shadows a
standard library name teaches the wrong thing.

### Vocabulary

Appended as an exemplar introduces a name. This is a record of what exists, not a
design fixed ahead of the code.

| Name | Layer | Introduced by |
|------|-------|---------------|
| `Temperature` | core | EXM-0001 |
| `DeviceId` | core | EXM-0001 |
| `SampleInterval` | core | EXM-0001 |
| `Registration`, `Registry` | device | EXM-0002 |
| `resolve_endpoint` | device | EXM-0002 |
| `SampleBuffer` | core | EXM-0003 |
| `DeviceFile` | device | EXM-0004 |
| `Clock` | device | EXM-0005 |
| `ReadingSink`, `StampedReading` | device | EXM-0005 |
| `Sampler` | device | EXM-0005 |
| `Reading`, `DecodeError` | wire | EXM-0006 |
| `parse_frame`, `reading_to_frame` | wire | EXM-0006 |
| `Calibration` | core | EXM-0007 |
| `try_calibrated_temperature` | core | EXM-0007 |
| `DeviceState`, `Offline`, `Idle`, `Sampling`, `Faulted` | core | EXM-0008 |
| `Health`, `state_to_health`, `format_state`, `format_health` | core | EXM-0008 |
| `SampleWindow`, `try_mean_temperature` | core | EXM-0009 |
| `LogLevel`, `write_log` | core | EXM-0010 |
| `SampleChannel`, `Poller` | device | EXM-0010 |
| `LatestReading` | device | EXM-0011 |
| `SampleLoop` | device | EXM-0012 |
| `sampler_driver_*` | ffi | EXM-0013 |
| `DriverFailure`, `DriverError`, `DriverSession` | ffi | EXM-0013 |
| `status_to_failure`, `format_frame` | ffi | EXM-0013 |
| `ReadSlot`, `ReadTask`, `load_reading` | device | EXM-0014 |

## Structural invariants

Enforced by `polc check`, which fails the build on any of them:

- `id` is unique across the layer and matches the directory prefix
- `demonstrates` is present, non-empty, and every entry resolves to an existing
  policy or standard entry, never to an anti-pattern
- every exemplar has at least one `*_test.cpp` in its tree, and every non-test
  `<layer>/<name>.cpp` has a `<layer>/<name>_test.cpp` beside it and a declaring
  header at `include/<project>/<layer>/<name>.hpp` or `<layer>/<name>.hpp`
- every `EXM-*` directory holds an `exemplar.md`, whose frontmatter carries no key
  beyond `id`, `demonstrates`, and `applicability`
- no body heading sits at `#` or `##`, the levels the statement renders into

The check runs from source to header and never the reverse, so EXM-0013's foreign C
ABI header `include/sampler/ffi/driver.h` needs no implementation in the tree.

Asserted by the format. Nothing checks them:

- every exemplar compiles clean under the configurations its `applicability` admits,
  at the warning set [STD-0024](../standard/STD-0024-warning-set.md) fixes, and its
  tests pass
- `applicability` records the floor of the facilities the code uses, so an exemplar
  reaching above C++14 carries a mark
- a canonical scalar value type has exactly one owning exemplar and is copied
  verbatim elsewhere
