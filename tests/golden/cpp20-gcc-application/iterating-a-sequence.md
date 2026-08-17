cpp20-gcc-application › Iterating a sequence

Read when: walking a container — whether a loop is the right shape at all, how the element is bound, what may not change while iterating.

## MUST — Prefer a named standard algorithm to a hand-written loop

POL-0098 · CG ES.71, CG SL.con.1

```cpp
// Never. The reader reconstructs "first tool wide enough" from the body.
const Tool* found = nullptr;
for (std::size_t i = 0; i < tools.size(); ++i) {
    if (tools[i].diameter_mm >= required_mm) { found = &tools[i]; break; }
}

// Right. The name is the intent.
const auto found = std::ranges::find_if(
    tools, [required_mm](const Tool& t) { return t.diameter_mm >= required_mm; });
```

On C++20 prefer the `std::ranges` overloads: passing the container once removes
the mismatched-iterator-pair failure mode. Below C++20 the iterator pair is the
only spelling.

Where no algorithm fits, use range-`for` rather than an index loop. Reach for
an index only when the index itself is part of the computation.

An index loop makes the reader derive the intent from the mechanism, which is
the inversion POL-0006 names. It also carries the bound, the comparison, and
the increment as three separate things to get wrong, and off-by-one lives in
all three. A named algorithm has none of them and states in its name what the
loop would have had to be read to discover.

## NEVER — Never insert into or erase from a container while iterating it

POL-0100

```cpp
// Never. erase() invalidates it; the next ++it is undefined.
for (auto it = moves.begin(); it != moves.end(); ++it) {
    if (it->is_empty()) { moves.erase(it); }
}

// Right. One pass, no invalidation to reason about.
std::erase_if(moves, [](const Move& m) { return m.is_empty(); });
```

Below C++20 the spelling is the erase-remove idiom,
`moves.erase(std::remove_if(moves.begin(), moves.end(), pred), moves.end())`.
Where elements must be added, build a second container and swap it in.

Invalidation rules differ per container, so the identical pattern is defined on
`std::list` and undefined on `std::vector`, and the code gives no sign of which
one it is. Worse, the undefined case usually appears to work: the freed
capacity is still mapped, so the loop completes and the corruption surfaces
somewhere else entirely. A whole-container operation states the intent and has
no iterator for the reader to track (POL-0098).

## NEVER — Never compute with a pointer

POL-0133 · CG Bounds.1, CG Bounds.2, CG ES.62, CG ES.65, CG Lifetime.1

```cpp
// Never. No bound, and the arithmetic is only valid within one array.
double sum(const double* first, const double* last) {
    double total = 0.0;
    for (const double* p = first; p != last; ++p) { total += *p; }
    return total;
}

// Right.
double sum(std::span<const double> values) {
    return std::accumulate(values.begin(), values.end(), 0.0);
}
```

Take a `std::span` and a standard algorithm (POL-0046, POL-0098). Index with a
constant expression or through an interface that carries the bound; a raw
subscript computed at runtime is the same defect in different syntax.

Comparing or subtracting pointers into different arrays is undefined even where
both are valid, so the comparison a bounds check depends on may not mean what it
says.

Pointer arithmetic is the one construction where the language provides neither a
check nor a diagnostic. Reading one element past the end is undefined behaviour
that usually succeeds, because the memory is mapped and holds something
plausible, so the failure surfaces as a wrong answer far from the loop
(POL-0002). A `std::span` carries the length the pointer form left in a comment,
and every standard algorithm over it derives its bound from the object rather
than from the caller remembering.

## MUST — A range-`for` binds `const auto&` to read and `auto&` to modify

POL-0099 · CG ES.71

```cpp
for (const auto& tool : tools) { total += tool.diameter_mm; }  // read
for (auto& tool : tools) { tool.wear += 1; }                   // modify
for (auto tool : tools) { tool.wear += 1; }                    // copies; the write is lost
```

A bare `auto` is written only where a copy is the point, and then the copy is
what the body is for.

`auto&&` is reserved for a generic context or a range whose yield is a proxy,
which is the same boundary POL-0050 draws around `auto` generally.

A bare `auto` copies every element, which is two defects at once. When the body
writes, the write lands on the copy and is discarded with no diagnostic, so the
loop runs and does nothing. When the body only reads, the copy is silent cost
proportional to the container. The binding is the only place the difference is
visible, so it has to state which of the three cases this loop is.
