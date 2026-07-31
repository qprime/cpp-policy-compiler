# Testimony: Coding Rules from live study sessions

**Captured:** 2026-07-31 | **Nature:** original testimony — this repo is the
source of record.

Distilled residue of live study sessions in the modern-cpp KB (sessions of
2026-07-30, KB commits `e1f65f3` and `109c9ae`). Each rule states the
directive and its why on one line, written to be handed to an AI coding
agent. Recorded verbatim.

## Lambdas

1. **Prefer a named function; use a lambda only for trivial glue at a single call site.** *Why:* lambdas buy locality, not brevity — justified only when inlining reads better than jumping to a name. If it wants a name, a doc comment, or a second use, it's a function.
2. **Ban default captures `[=]` and `[&]`; capture each variable explicitly.** *Why:* the capture list is the one part with lifetime consequences — an explicit list makes the ownership decision auditable at a glance; defaults hide what state the lambda carries.
3. **A lambda that is stored, returned, or passed to another thread must capture by value (or explicit ownership transfer), never by reference.** *Why:* by-reference capture is a non-owning observer, valid only while the captured object outlives the lambda; if the lambda escapes its scope, by-reference dangles and the compiler won't catch it.
4. **Allow by-reference capture only for a lambda that runs and dies within the current scope** (the algorithm-comparator case). *Why:* it can't outlive what it borrows, so it's safe and avoids a copy.
5. **Never capture `[this]` in a lambda that outlives the object.** *Why:* `[this]` is a hidden lifetime dependency on the enclosing object; if the callable is stored and the object dies, every call dereferences a dead `this`. Prefer capturing specific members by value, or a `weak_ptr` you lock.

## auto

1. **Prefer `auto` (owns) or `const auto&` (reads) for concrete values; reserve `auto&&` for range-for and generic forwarding.** *Why:* on a hand-written concrete line the type is known, so bare `auto&&` buys nothing and hides intent — it only earns its keep binding unpredictable range/proxy yields or forwarding an unknown type onward. Any other bare `auto&&` is a flag for review.
