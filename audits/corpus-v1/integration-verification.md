# Issue 36: exemplar and final integration verification

This gate reviews the corpus after issues 29–35 and their follow-up corrections.
The inventory contains 248 policies (including the later POL-0249), 29 standard
entries, and 14 exemplars. The original issue's 247-policy count predates that
addition. All 291 identities have resolved dispositions. No compiler invariant,
configuration field, stable identity, or replacement edge changes in this gate.

## Complete-tree review

Every exemplar's headers, implementation, adjacent tests, and fixtures were
inspected, including the eleven identical Temperature copies. The report's
`related_ids` records every inspected `demonstrates` identity. Declarations and
implementation supply structural evidence; tests supply observable behavior.
Style identities are demonstrated by source shape, not inferred from test success.
All claims remain supported; no identity is split, removed, or relabeled.

| Exemplar | Evidence and assumptions checked |
|---|---|
| EXM-0001 | Validated finite Temperature, constructor/optional failure distinction, comparisons, adjacent Catch2 tests, named units and class layout. |
| EXM-0002 | Public registry and private implementation headers, DeviceId invariant, endpoint resolution, duplicate-ID rejection and optional lookup; C++20 string operations. |
| EXM-0003 | Bounded vector storage, reserved capacity, eviction order, value semantics and behavior tests; ordinary owning use, not a hard deadline guarantee for moved-from instances. |
| EXM-0004 | POSIX open/close ownership, invalid descriptor sentinel, deleted copies, move transfer and self-assignment; assumes a POSIX platform, not portable ISO file-descriptor APIs. |
| EXM-0005 | Non-owning clock/sink pointers, reference constructor contract, virtual collaborator interfaces, timestamp tests; collaborators must outlive the sampler. |
| EXM-0006 | Span bounds, big-endian unsigned assembly, bit_cast, named decoding errors and semantic wire round trip; C++23 expected, eight-bit bytes and binary32 float. Named expected-based encoding failures, bounds and quantization are explicit. |
| EXM-0007 | Finite positive calibration scale, finite offset, nonempty-span precondition, optional domain failures, named reduction helpers and behavior assertions. Running mean avoids avoidable sum overflow. |
| EXM-0008 | Tagged alternatives, exhaustive visit overloads, named enum formatting, jumping switch arms and invalid-enumerator diagnostics; no unmarked fallthrough. |
| EXM-0009 | Span/transform/filter/accumulate, named finite window invariant, explicit captures and empty-result absence. Running mean preserves finite range without overflowing a sum. |
| EXM-0010 | jthread constructed after its dependencies, stop-aware wait, joined destruction, owned channel synchronization and cancellation tests; logging and waits make this an ordinary worker, not a deadline path. |
| EXM-0011 | Mutex protects the queue predicate and storage, condition-variable wait loop, optional timeout result, bounded capacity, multithread behavior tests; tests are not a proof of arbitrary scheduling. |
| EXM-0012 | Constructor reserve, capacity guard, noexcept scan, no locks/logs/I/O and counted allocator calls; realtime applicability remains, but deadline compliance requires bounded input and target timing. |
| EXM-0013 | C-compatible header, foreign handle ownership, status translation, expected failures, C-string boundary conversion in the fake provider and golden serialization. Fake ABI tests cover pointer checks and serial sessions, not a production driver. |
| EXM-0014 | Owning frame parameter, weak promise reference, all five handle special members, continuation disconnection before destruction, ready/suspended paths and promise exceptions; single-threaded, one pending reader. |

Regressions for oversized wire values, overflowing collection means, non-finite
window bounds, scaled large calibration samples, and duplicate coroutine readers
failed before their fixes and pass afterward. A null-slot regression also passes.
The C++ floating conversion specification makes conversion outside the target
range undefined; the guard precedes that conversion. `std::lerp` guarantees a
finite result for finite endpoints and a weight in [0, 1]. Await-suspend exceptions
leave the existing slot registration intact and reach the coroutine promise.
Primary sources: [floating conversions](https://eel.is/c++draft/conv.double),
[lerp](https://eel.is/c++draft/c.math.lerp),
[await expressions](https://eel.is/c++draft/expr.await), and
[coroutine definitions](https://eel.is/c++draft/dcl.fct.def.coroutine).

## Reproduce executable checks

Use Python 3.12+, uv, CMake 3.20+, GCC 13 or another toolchain with the required
C++20/C++23 library facilities, and an installed Catch2 3. This run used GCC 13.3,
CMake 3.28 and Catch2 3.8.1. To install the exact test dependency locally:

```sh
git clone --depth 1 --branch v3.8.1 https://github.com/catchorg/Catch2.git /tmp/polc-catch2
cmake -S /tmp/polc-catch2 -B /tmp/polc-catch2/build -DCMAKE_INSTALL_PREFIX=/tmp/polc-catch2/install -DCATCH_BUILD_TESTING=OFF -DCATCH_INSTALL_DOCS=OFF -DCATCH_INSTALL_EXTRAS=OFF
cmake --build /tmp/polc-catch2/build --parallel 4
cmake --install /tmp/polc-catch2/build
uv run python scripts/check_exemplars.py --build-dir /tmp/polc-exemplars --catch2-prefix /tmp/polc-catch2/install --jobs 4
uv run pytest -q
uv run polc audit check --root audits/corpus-v1 --final
uv run polc eval run benchmarks/generation/first-write.yaml --out /tmp/polc-generation.json
uv run polc eval run benchmarks/review/seeded-defects.yaml --out /tmp/polc-review.json
uv run python scripts/check_release_reproducibility.py --out /tmp/polc-release-check
```

The runner builds every production and test translation unit at the minimum
declared C++ version, with the project warning set and warnings as errors, links
the real Catch2 test library, and executes all 14 suites. A fifteenth executable
checks the shared driver header under C11. The golden test runs from its exemplar
root. This is stronger evidence than the earlier production-only syntax checks.
The release check requires a new output directory, builds two wheels, installs
each into a separate environment, and builds the two stock archives outside the
checkout. It compares artifact names and SHA-256 hashes and fails on disagreement.

Build all four stock projections for inspection:

```sh
for config in cpp20-gcc-application cpp23-gcc-realtime; do
    for mode in generation review; do
        uv run polc build --config "docs/configurations/$config.md" --mode "$mode" --out "/tmp/polc-$config-$mode"
    done
done
```

Inspect each topic's rendered entries, the decided-once standard, and all admitted
exemplar directories against source. Generation projections contain admitted
exemplars and their provenance; review projections exclude exemplar documents
and source copies while retaining admitted exemplar metadata in provenance. Domain and
language filtering may omit exemplars, especially C++23 expected-based examples
and the realtime-only loop. Omission is not loss of a canonical identity.

## Evidence boundaries

Results: 55 Python tests; 15 executable CTest checks; final audit coverage; four
stock projections; both deterministic recorded evaluator runs; and matching
wheel and stock-archive hashes across two builds. The cross-slice ledger records
the resolved fixes. Original slice reports retain earlier semantic review
provenance; integration rechecks affected exemplar relationships against those
policies and standards. Missing policy review routes remain explicit compiler
diagnostics rather than invented routing evidence.

Recorded evaluator results and the historical Relay experiment do not measure
the effect of this wording on a new model run. No live or paid model trial was
launched. This gate makes no model-effectiveness claim needing a new benchmark
issue. Future such claims require a focused hypothesis, versioned fixture, judge
rubric, comparison and stopping rule. No unresolved minor finding is accepted.

## Compared artifact hashes

```text
447361471ff62042b8a938be59f35cc6a362c3d7b195adfb268a1c7c2dfc3553  polc-0.1.0-py3-none-any.whl
4b97ace8cd96eb58e622987a1a66ece9fbda042f5cf3d2eaa3d554c1cd30c333  cpp20-gcc-application-polc-0.1.0.zip
d71a61033c70313e82eed847dcc633fb25dc22143646bc24c10630317809c86a  cpp23-gcc-realtime-polc-0.1.0.zip
```
