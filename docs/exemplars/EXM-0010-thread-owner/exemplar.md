---
id: EXM-0010
demonstrates:
  - POL-0053
  - POL-0054
  - POL-0071
  - POL-0082
  - POL-0163
  - POL-0165
  - POL-0169
  - POL-0171
  - POL-0172
  - POL-0173
  - POL-0174
  - POL-0175
  - POL-0176
  - POL-0225
  - POL-0226
  - POL-0240
  - POL-0244
  - POL-0245
  - POL-0248
  - STD-0009
applicability:
  language_version: ["20", "23"]
---

# One object owning one thread, one channel, and the shutdown between them

`Poller` runs a thread and owns everything that thread touches: the interval it
paces by, the channel it writes into, and the flag it sets on the way out. Nothing
is reached for and nothing is detached. `worker_` is declared last, so it is
destroyed first, and the channel it writes into is still alive while it winds down.

The exit flag is a `std::shared_ptr<std::atomic<bool>>` so a caller can still read it
after the `Poller` is gone. That is what makes
`destructor_joins_the_running_thread` an observable claim rather than an assertion
about code the test cannot see.

This is the only exemplar where logging appears. `INFO` carries the two lines an
operator wants, and the dropped sample is `WARN` because it is unexpected and the
poller carries on.

## Reading order

- `include/sampler/core/log.hpp`, `core/log.cpp` — the one module that owns a
  stream, and `'\n'` rather than `std::endl`
- `include/sampler/device/sample_channel.hpp` — a mutex declared with the deque it
  guards and nothing else, under a stated threading model
- `device/sample_channel.cpp` — the lock as a named RAII object, `notify_one`
  outside the critical section, and a wait that names its condition
- `include/sampler/device/poller.hpp` — the five special members, and `worker_`
  declared after everything the thread uses
- `device/poller.cpp` — the lambda capturing `this` explicitly, the loop condition
  saying when it stops, and the channel pushed to outside the tick lock
- `device/poller_test.cpp` — shutdown by request and shutdown by destruction, each
  observed through the flag
- `include/sampler/core/temperature.hpp`,
  `include/sampler/core/sample_interval.hpp`, and their sources and tests — copied
  verbatim from EXM-0001
