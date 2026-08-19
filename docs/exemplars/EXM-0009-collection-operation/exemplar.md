---
id: EXM-0009
demonstrates:
  - POL-0013
  - POL-0033
  - POL-0035
  - POL-0041
  - POL-0053
  - POL-0056
  - POL-0058
  - POL-0136
  - POL-0183
  - POL-0203
  - POL-0228
  - POL-0229
  - POL-0240
  - POL-0244
  - POL-0245
  - POL-0247
  - STD-0011
  - STD-0012
applicability:
  language_version: ["20", "23"]
---

# Filter, then reduce, with the empty result reported as absence

`try_mean_temperature` composes two views and accumulates over the result. A window
that admits nothing is not an error and not a zero; it is a mean that does not
exist, which is what `std::optional` says.

The window bounds stay `double` with unit-suffixed names rather than becoming
wrapped types, because arithmetic flows straight through them. The invariant they
do carry — lowest at or below highest — is what makes the window a class.

`within_celsius` is not `const`. A `filter_view` caches the position of its first
element on the first traversal, so `begin()` is non-`const` and a `const` view is
unusable.

## Reading order

- `include/sampler/core/reading_stats.hpp` — the bounds as named primitives, the
  predicate under the standard library's name for it, and a `try_` that returns
  absence
- `core/reading_stats.cpp` — transform and filter composed before anything is
  summed, each lambda naming its captures
- `core/reading_stats_test.cpp` — a fixture holding the window, `GENERATE` over
  three shapes of empty result, and `filters_before_reducing` asserting the mean
  itself so that reducing before filtering fails it
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001
