---
id: EXM-0011
demonstrates:
  - POL-0053
  - POL-0126
  - POL-0133
  - POL-0163
  - POL-0165
  - POL-0169
  - POL-0172
  - POL-0176
  - POL-0183
  - POL-0240
  - POL-0244
  - POL-0245
  - STD-0019
applicability:
  language_version: ["20", "23"]
---

# One guarded value, reached by several threads, owned by none of them

`LatestReading` is the whole shared mutable state: one mutex, one optional, and two
operations that each take the lock and return. It starts no thread and joins none —
the threads belong to whoever uses it, which in this exemplar is the test.

The mutex is `mutable` so the reader can be `const`. That is the case
POL-0126 leaves open for a cache, and it is the only `mutable` in the corpus.

`two_writers_and_a_reader_complete_without_deadlock` claims exactly what its name
says. Three threads finish and the settled value is one of the two that were
written. It establishes nothing about the absence of races, which no passing run
can establish; that property is carried by the fact that every path to `reading_`
goes through the lock.

### Reading order

- `include/sampler/device/latest_reading.hpp` — the threading model stated in the
  header, and a private section holding the mutex and exactly what it guards
- `device/latest_reading.cpp` — two functions, each a named lock and one statement
- `device/latest_reading_test.cpp` — the joining threads scoped so that the
  assertions run after all three have finished
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001
