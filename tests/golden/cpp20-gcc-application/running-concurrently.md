cpp20-gcc-application › Running concurrently

Read when: a threading model exists and shared state has to be reached from more than one thread.

## THIS WAY — Concurrency mechanism

POL-0105 · CG CP.110

Reached only once a threading model exists. POL-0049 governs whether one should.

| Need | Mechanism |
|------|-----------|
| Shared primitive: counter, flag, single-pointer handoff | `std::atomic<T>` |
| Compound shared state | `std::mutex` under a scoped lock |
| Read-heavy access, measured rather than assumed | `std::shared_mutex` |
| Wait / notify | `std::latch`, `std::barrier`, `atomic::wait`; `std::condition_variable` below C++20 |
| One-time initialization | `std::call_once`, or a function-local `static` |
| An owned thread | `std::jthread`; below C++20, a type that joins in its destructor |
| Pure functions over immutable data | nothing |

```cpp
class ScanCounter {
 public:
    void record() { count_.fetch_add(1, std::memory_order_relaxed); }
    std::int64_t total() const { return count_.load(std::memory_order_relaxed); }
 private:
    std::atomic<std::int64_t> count_{0};
};
```

An atomic makes the single-value case correct without a critical section, and a
mutex is the only mechanism that makes several values change together. Choosing
between them is the whole decision, and reaching for the mutex by default costs
a lock the design did not need while reaching for the atomic by default leaves
compound state torn.

The wait and one-time-init rows exist because both have a hand-written form
that is a classic race: a predicate loop omitted against spurious wakeup, and
an initialized flag checked without synchronization. The language provides
both correctly, so neither is written by hand (POL-0008).

## NEVER — Never improvise synchronisation out of `volatile`, a flag, or a sleep

POL-0107 · CG CP.8

```cpp
// Never. volatile orders nothing between threads.
volatile bool ready_ = false;

// Never. Double-checked locking without atomics is a data race.
if (!initialised_) {
    const std::lock_guard<std::mutex> lock(m_);
    if (!initialised_) { init(); initialised_ = true; }
}

// Never. Waiting by guessing.
while (!ready_) { std::this_thread::sleep_for(std::chrono::milliseconds(10)); }
```

Take the mechanism the need selects (POL-0105): `std::atomic` for the flag,
`std::call_once` or a function-local `static` for the one-time init,
`std::latch` or `atomic::wait` for the wait.

`volatile` addresses memory that changes outside the program — a
memory-mapped device register. It orders nothing and prevents no reordering
between threads, so it looks like synchronisation and provides none.

All three test as working. A data race is undefined behaviour whose observable
result depends on the optimizer, the core count, and the load, so the version
that passed on a developer machine is not evidence about the deployment host.
The sleep is the same defect with a tunable failure rate, which invites raising
the number rather than fixing the wait.

## NEVER — Never keep thread-local global state

POL-0108

```cpp
// Never. Nothing in any signature says the result depends on which thread ran it.
thread_local ScanContext g_context;

void record(const Move& m) { g_context.moves.push_back(m); }

// Right. The dependency is a parameter.
void record(ScanContext& context, const Move& m) { context.moves.push_back(m); }
```

Where per-thread state is genuinely required, it lives in an explicit context
object created at the thread's entry point and passed into the functions that
need it.

Thread-local state is invisible in every signature that depends on it, so the
same call with the same arguments produces different results per thread and
nothing in the code says so. That defeats the determinism POL-0007 asks for and
makes the functions untestable in the ordinary way, because the test has to
reproduce which thread ran.

It also fails silently under a thread pool, where work migrates between threads
between calls and the state a function expects to find is the state some
unrelated task left behind.

## MUST — A mutex is locked by a scoped lock, never by hand

POL-0106 · CG CP.20, CG CP.21

```cpp
// Never. Every early return and every throw leaks the lock.
m_.lock();
if (entries_.empty()) { return {}; }
auto result = entries_.front();
m_.unlock();

// Right.
const std::lock_guard<std::mutex> lock(m_);
if (entries_.empty()) { return {}; }
return entries_.front();
```

Locking more than one mutex at once takes `std::scoped_lock` over all of them
in one statement.

A hand-managed lock is a resource released on one path and leaked on every
other, which is exactly the case POL-0003 answers with RAII. The failure is
worse than a leak: the mutex stays held, so the next thread to want it blocks
forever, and the deadlock surfaces far from the return that caused it.

Two sequential `lock_guard`s in different orders in two functions deadlock
whenever both run at once. `std::scoped_lock` orders the acquisition
internally, so the ordering cannot be got wrong at the call site and does not
have to be documented and remembered.

See also: [POL-0049 — Never add a mutex to a class with no threading model](structuring-modules-and-layers.md)
