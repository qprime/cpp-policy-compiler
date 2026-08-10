---
id: POL-0014
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Tier 1 #1"
    upstream: ["CG R.20", "CG R.21", "CG R.3", "CG R.4", "CG R.11"]
  - source: cpp-convention/conventions.md
    locator: "Pattern: ownership decision"
    upstream: ["CG I.11", "CG R.32"]
  - source: cpp-convention/mechanisms.md
    locator: "§3 Ownership"
---

# Ownership is single and explicit

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
