---
id: EXM-0014
situation: write a coroutine that suspends on a read and resumes with the value
demonstrates:
  - POL-0071
  - POL-0072
  - POL-0079
  - POL-0080
  - POL-0082
  - POL-0109
  - POL-0163
  - POL-0173
  - POL-0179
  - POL-0181
  - POL-0195
  - POL-0240
  - POL-0244
  - POL-0245
  - STD-0010
  - STD-0011
  - STD-0020
applicability:
  language_version: ["20", "23"]
---

# A coroutine that suspends on a device read and resumes with the value

`load_reading` takes its slot as a `std::shared_ptr` by value, so the frame owns a
share of the thing it suspends on and the slot cannot go away underneath it. A
reference parameter would not extend the slot's lifetime; it would require a
separate guarantee covering suspension and cancellation. Passing the owning
`shared_ptr` by value establishes that guarantee in this exemplar.

Nothing is locked across the `co_await`. There is no lock in this exemplar at all,
which is how the property is carried — no test asserts it, because none could.

`ReadTask` owns one coroutine handle and nothing else, and its five special members
follow from that. It is a concrete type rather than a `Task<T>`, because one return
type is one return type.

Destroying an unfinished task unregisters its continuation from the slot before
destroying the coroutine frame. The slot therefore never retains a handle to a dead
frame when cancellation precedes a later device write. Writes, suspension, and
cancellation are serialized on one thread; this is not a cross-thread race
protocol. A second suspended reader is rejected with `std::logic_error` without
disconnecting the first. A null slot reports `std::invalid_argument`. The promise
captures these exceptions and `get_reading()` rethrows them on a completed task.

### Reading order

- `include/sampler/device/async_read.hpp` — the awaitable's three functions, the
  promise type as a nested type ahead of the constructors, and a coroutine whose
  parameters are values
- `device/async_read.cpp` — the handle taken out of the slot before it is resumed,
  cancellation disconnecting the continuation, and the five special members of a
  handle owner
- `device/async_read_test.cpp` — resumption observed through the task, the
  already-ready path that never suspends, and the share count showing the frame
  took a copy, cancellation before a later write, duplicate-reader rejection,
  and null-slot failure
- `include/sampler/core/temperature.hpp`, `core/temperature.cpp`,
  `core/temperature_test.cpp` — copied verbatim from EXM-0001
