cpp20-gcc-application › Structuring modules and layers

Read when: laying out headers, includes, namespaces, dependency direction, or a threading model.

## MUST — Dependency direction holds

POL-0018

Includes flow one way through the layer stack. A layer may include from layers
downstream of it, never from layers upstream.

```
Input/CLI  →  Parser  →  IR/Model  →  Validation  →  Backend/Output
```

The test for an ambiguous case: delete the higher-level module mentally, and ask
whether the lower-level modules still compile. If they do not, the dependency is
already inverted and the include that inverted it is the defect.

A lower layer that needs a higher layer's type gets an adapter at the boundary
(POL-0087). Pulling the higher layer's headers down is what the rule forbids.

An inverted include is not visible in the file that contains it; it is visible
only in the shape of the whole graph, which no single edit shows. Once the graph
has a cycle, the layers can no longer be built, tested, or reasoned about
separately, and the cost of restoring the direction grows with every edge added
after. The rule is stated as a direction rather than as a set of allowed pairs
so that it holds for layers that do not exist yet.

## THIS WAY — Module boundary

POL-0028 · CG SF.2, CG SF.5, CG SF.7, CG SF.8, CG SF.11, CG SF.20, CG SF.21, CG SF.22

A header is an interface. What it exposes is a promise; what it hides is free to
change.

```cpp
// include/proj/store/compact.hpp
#ifndef PROJ_STORE_COMPACT_HPP
#define PROJ_STORE_COMPACT_HPP

#include <vector>
#include "proj/types.hpp"

namespace proj::store {

Result compact(const Store& store, const CompactParams& params);

}  // namespace proj::store

#endif  // PROJ_STORE_COMPACT_HPP
```

```cpp
// store/compact.cpp
#include "proj/store/compact.hpp"

namespace proj::store {
namespace {

constexpr int kMaxPassCount = 8;
Result compact_incremental(const Store& store, const CompactParams& params);

}  // namespace
}  // namespace proj::store
```

| Rule | |
|------|--|
| Internal entities live in an anonymous namespace in the `.cpp` | `CG SF.22` |
| Never an anonymous namespace in a header | `CG SF.21` |
| A header is self-contained and compiles alone | `CG SF.11` |
| No object definitions or non-inline function definitions in a header | `CG SF.2` |
| A `.cpp` includes the header declaring its own interface, first | `CG SF.5` |
| No `using namespace` at header scope | `CG SF.7` |
| An `#ifndef` include guard on every header, named `PROJECT_COMPONENT_FILE_HPP`; `#pragma once` is a non-standard vendor extension and is not used | `CG SF.8` |
| Namespaces express logical structure, nested by layer | `CG SF.20` |

Where a module's threading model is not obvious from its declarations, it is
stated in one or two sentences at the top of the header. That statement is what
POL-0049 asks for in place of a defensive mutex; the default it overrides is
single-threaded by contract.

The test for a leaky header: if changing a private implementation detail forces
unrelated translation units to recompile, the detail is in the wrong file.

Everything a header declares is something every consumer now depends on, whether
or not any of them use it. That dependency is invisible at the point it is
created and expensive at every point it is later discovered, because removing a
declaration means finding every file that reached for it. Keeping the header to
the promise is what makes the implementation changeable without a survey of
consumers.

## NEVER — Never add a mutex to a class with no threading model

POL-0049

A `std::mutex` member on a class nobody shares across threads protects nothing.
The default for every type is single-threaded by contract, and concurrent access
is the caller's problem until the type says otherwise.

```cpp
// Never: locks every accessor, documents nothing, and is not thread-safe anyway
class Registry {
 public:
    void add(Entry e) { std::lock_guard<std::mutex> lock(m_); entries_.push_back(std::move(e)); }
    std::vector<Entry> all() const { std::lock_guard<std::mutex> lock(m_); return entries_; }
 private:
    mutable std::mutex m_;
    std::vector<Entry> entries_;
};
```

Write nothing, and state the threading model at the module boundary when
concurrency is actually introduced (POL-0028).

A per-method lock makes each method atomic and makes nothing else atomic, so any
caller reading and then writing still races. The type is now advertised as
thread-safe, which is the claim that causes the race to be written. It costs a
lock on every access, it costs the reader an assumption about a model that was
never designed, and it removes the pressure to design one, because the mutex
looks like the design.

## MUST — A lower layer that needs a higher layer's type gets an adapter

POL-0087

Where a lower layer needs something a higher layer knows, an adapter at the
boundary converts it into a type the lower layer already owns. The higher
layer's headers do not come down (POL-0018).

Three forms, in order of preference:

1. The lower layer declares the type it needs, and the higher layer supplies a
   value of it.
2. The lower layer takes a callback or an interface it declares, which the
   higher layer implements.
3. An adapter type at the boundary translates between the two.

The first is usually available and usually skipped, because pulling the existing
type down is one line and declaring a new one is several.

An include added to satisfy one call permanently attaches everything else that
header declares, and the attachment is invisible from the line that created it.
The lower layer then cannot be built, tested, or reused without the higher one,
which is the specific loss the direction rule exists to prevent. An adapter costs
a type and a conversion and confines the knowledge of both layers to one file,
which is also the file to change when either side moves.

## SHOULD — A wrapper type lives at the layer that owns its precondition

POL-0088

Where several layers use a wrapper type (POL-0027), it is defined at the layer
that establishes the precondition, not at the layer that consumes the value.

The owning layer is the one that can produce the type: the one holding the
validation, the parsing, or the invariant that makes the conversion possible.
Consumers depend on it in the permitted direction (POL-0018).

Where two layers both appear to establish it, the precondition is being checked
twice and one of the checks is redundant (POL-0045). Resolve that before placing
the type.

Placing the type with a consumer inverts the dependency the moment a second
consumer appears, because the second one has no reason to depend on the first.
The producing layer then either includes downward to construct the type or hands
back an unvalidated value, and both undo the guarantee the wrapper existed for.
Placing it with the producer makes the type available to every consumer along
the direction includes already flow, so adding a consumer costs nothing
structural.
