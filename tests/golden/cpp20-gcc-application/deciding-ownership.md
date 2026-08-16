cpp20-gcc-application › Deciding ownership

Read when: deciding who owns an allocation or resource and how the declaration says so.

## MUST — Ownership is single and explicit

POL-0014 · CG R.20, CG R.21, CG R.3, CG R.4, CG R.11, CG I.11, CG R.32

Every allocation has exactly one owner, and which one it is must be answerable
from the declaration alone. A raw pointer or a reference is non-owning in every
standard, with no exception.

| Need | Form |
|------|------|
| Exclusive ownership | `std::unique_ptr<T>`, transferred by move |
| Construct the owned object | `std::make_unique` from C++14; a C++11 project writes `unique_ptr<T>(new T(...))` once, inside a factory |
| Shared ownership, genuinely | `std::shared_ptr<T>` |
| Break a `shared_ptr` cycle | `std::weak_ptr<T>` |
| Observe without owning | `T&`, or `T*` where null is meaningful |

POL-0024 carries the procedure for choosing among these. Ownership never
transfers through a raw pointer: a function taking `std::unique_ptr<T>` by value
assumes ownership and its signature is what says so.

Banned in every standard: `std::auto_ptr`, owning raw pointers, `malloc` and
`free` in C++ code, and `new` or `delete` outside a resource-management
function.

Two owners is a double release and no owner is a leak. Both are decided at the
point of allocation and paid somewhere else entirely, usually in a translation
unit whose author never saw the allocation. Naming the owner in the type is what
makes the release automatic, which reduces the sites that can get lifetime wrong
to the sites that declare an owner.

## THIS WAY — Ownership decision

POL-0024 · CG R.3, CG R.4, CG R.5, CG R.20, CG R.21, CG F.60

Four questions, in order. The first *yes* is the answer.

| Question | Answer |
|----------|--------|
| Does this need to outlive the current scope? | **No** → a value or an automatic variable. Do not heap-allocate. |
| Is there exactly one owner? | **Yes** → `std::unique_ptr<T>`, transferred by move. |
| Are there genuinely multiple independent owners with no primary? | **Yes** → `std::shared_ptr<T>`. |
| None of the above; you only need to look at it | `const T&`, or `T*` where null is meaningful. Non-owning, always. |

Most code stops at the first question. A value member, a `std::vector<T>`, and a
`const&` parameter cover the large majority of real ownership needs, and they
are the forms that leave no lifetime question to answer.

Answer the questions in order rather than reaching for the form that always
works. `std::shared_ptr` always works, which is why it is what an unresolved
ownership question turns into (POL-0048): the design keeps compiling and the
question stops being asked. Asking in this order forces the cheapest correct
answer, and it makes the expensive one a decision somebody made rather than a
default nobody noticed.

## NEVER — Never reach for `shared_ptr` because the ownership question is open

POL-0048 · CG R.21

`std::shared_ptr` is for genuinely shared ownership: several independent owners
with no primary among them. Reaching for it because it is the form that always
compiles hides the question it was supposed to answer.

Work the ownership decision instead (POL-0024). Most values need no heap at all,
and most that do have exactly one owner.

```cpp
std::shared_ptr<Store> store;   // why is it shared? nothing here says
std::unique_ptr<Store> store;   // one owner, transferred by move
Store store;                    // most often this
```

What is bought is an atomic refcount on every copy and a lifetime that ends at a
moment no single piece of code decides. What is lost is the question: a
`shared_ptr` in a declaration reads as a design decision, so the next reader
assumes sharing was required and writes code that requires it. That is how a
placeholder becomes load-bearing, and by then the cost of asking again is the
cost of tracing every copy.
