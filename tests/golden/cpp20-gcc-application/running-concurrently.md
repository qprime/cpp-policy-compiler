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

## NEVER — Never hand-write a lock-free data structure

POL-0143 · CG CP.100, CG CP.101, CG CP.102

```cpp
// Never. A hand-rolled compare-and-swap stack: the ABA problem, the reclamation
// problem, and the memory-ordering problem, none of which a test will show.
void push(Node* n) {
    do { n->next = head_.load(std::memory_order_relaxed); }
    while (!head_.compare_exchange_weak(n->next, n));
}
```

Take a mutex (POL-0105). A single `std::atomic<T>` with the default sequentially
consistent ordering is not this anti-pattern — it is the shared-primitive row of
the mechanism table, and it is fine.

What is excluded is a data structure built out of compare-and-swap loops,
explicit `memory_order` relaxation, or any published algorithm reproduced from
memory.

Lock-free code fails in ways testing does not reach. The defects are
interleavings that occur under a load the test never applied, on a core count
the test machine did not have, or only after the optimizer reorders operations
the relaxed ordering permitted it to reorder. A run that passes is not evidence,
which puts this outside what POL-0001 can offer — neither the type system nor
the test suite constrains it.

The payoff is a constant factor on contention. The cost is a class of defect
that is undetectable in review, unreproducible in the field, and correct only if
the author's memory-ordering reasoning was right the first time.

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

## SHOULD — Concurrency is expressed as tasks with results, not as threads with side effects

POL-0138 · CG CP.4, CG CP.41, CG CP.60, CG CP.61

```cpp
// Avoid. A thread, a shared buffer, and a lock to protect what is really a return value.
std::vector<Plan> results;
std::mutex m;
std::thread t([&] { auto p = plan(pocket); std::lock_guard lk(m); results.push_back(p); });

// Prefer. The result comes back through the type system.
auto future = std::async(std::launch::async, plan, pocket);
const auto p = future.get();
```

Prefer a pool or `std::async` to creating and destroying threads per unit of
work. Thread creation is expensive relative to most tasks, and a thread per item
turns a bounded workload into unbounded contention.

A task returns its result through a `std::future`, which means the answer
crosses the thread boundary as a value rather than as shared mutable state
someone has to lock, publish, and remember to read.

Thinking in threads makes every result a side effect on state two threads can
see, which is the sharing POL-0105 then has to protect. Thinking in tasks
removes most of that state: what would have been a guarded buffer becomes a
return type, and the concurrency question shrinks to what genuinely must be
shared (POL-0124).

## MUST — Every thread is owned by a scope that joins it

POL-0139 · CG CP.23, CG CP.24, CG CP.26

```cpp
// Never. Nothing waits for it, and nothing knows what it still refers to.
std::thread(scan_loop, std::ref(context)).detach();

// Right, on C++20. Joins in its destructor, on every path out.
std::jthread worker(scan_loop, std::ref(context));
```

Below C++20 the equivalent is a type holding a `std::thread` that joins in its
destructor, which is POL-0003 applied to a thread.

Never `detach()`. A detached thread outlives every scope, so it is a global with
an execution context attached, and it may still be running while the objects it
captured are destroyed during shutdown.

A joining thread is a scoped container: what it borrows must outlive the join,
and the join is what proves it. A detached one is unbounded, and no reader can
say what is still alive when the process exits.

A `std::thread` destroyed while still joinable calls `std::terminate`. That
turns any exception on the path between construction and `join()` into a process
abort, so the failure mode of forgetting the join is not a leak but a crash with
no unwinding and no diagnostic pointing at the thread.

## MUST — A lock is named, held briefly, and never held across a call you do not control

POL-0140 · CG CP.22, CG CP.43, CG CP.44

```cpp
// Never. The callback may lock something else, re-enter, or block indefinitely.
{
    const std::lock_guard lock(m_);
    for (const auto& observer : observers_) { observer.on_change(state_); }
}

// Right. Copy what is needed, release, then call out.
std::vector<Observer> targets;
{
    const std::lock_guard lock(m_);
    targets = observers_;
}
for (const auto& observer : targets) { observer.on_change(state_); }
```

Every lock object has a name. `std::lock_guard(m_)` without one is a temporary
that is destroyed at the end of the full expression, so it locks and immediately
unlocks and the section that follows is unprotected. Nothing warns.

Do only what the shared state requires while holding the lock. Formatting,
allocation, and input or output belong outside it.

An unknown callee under a lock is the general case of deadlock: it may acquire a
second mutex in the opposite order to some other path (POL-0106), it may block
on input, or it may re-enter this object and try to take the same lock. None of
that is visible from the call, because the callee is chosen by whoever
registered it.

A long critical section serializes every other thread onto this one, which
converts a concurrency design into a sequential one that also pays for locking.

## THIS WAY — Guarded state

POL-0141 · CG CP.50

```cpp
class ToolCache {
 public:
    std::optional<Tool> find(ToolId id) const {
        const std::lock_guard lock(guard_.m);
        const auto it = guard_.by_id.find(id);
        return it == guard_.by_id.end() ? std::nullopt : std::optional{it->second};
    }

 private:
    struct Guarded {
        mutable std::mutex m;
        std::unordered_map<ToolId, Tool> by_id;
    };
    Guarded guard_;
};
```

The mutex and everything it protects sit in one nested structure, declared
together. What the lock covers is then a fact about the declaration rather than
a convention a reader has to infer from which members happen to be touched under
it.

A mutex declared beside unrelated members says nothing about its scope. The
protected set lives in whoever wrote the locking, and it drifts the first time a
member is added — nobody can tell from the declaration whether the new one
belongs inside the lock, so half the accessors take it and half do not.

This applies only where POL-0049 has established that a threading model exists,
and it does not make the type thread-safe on its own: a caller that reads and
then writes still races unless the compound operation is itself a method
(POL-0105).

## MUST — Small data crosses a thread boundary by value; shared ownership is `shared_ptr`

POL-0142 · CG CP.31, CG CP.32

```cpp
// Never. The caller's frame may be gone before the task reads it.
std::jthread worker([&request] { handle(request); });

// Right. The task owns its input.
std::jthread worker([request] { handle(request); });

// Right, where two unrelated threads genuinely both own it.
auto table = std::make_shared<const ToolTable>(load_tools(path));
std::jthread worker([table] { plan_with(*table); });
```

By value is the default: a copy removes the lifetime question and the
synchronization question at once, and for small data it costs less than the lock
that would otherwise be needed.

Where the data is large or genuinely shared between threads with no clear
primary owner, `std::shared_ptr` is the mechanism — this is the case POL-0048
holds it open for. Prefer `shared_ptr<const T>`, so sharing does not also mean
shared mutation.

A reference passed to another thread is a lifetime claim that no signature
states and no compiler checks: the referent must outlive a thread whose end the
caller may not wait for. When it does not, the read is undefined and lands
wherever that memory has been reused, which is the failure POL-0002 ranks worst
because nothing downstream can tell it from a correct value.

See also: [POL-0049 — Never add a mutex to a class with no threading model](structuring-modules-and-layers.md)
