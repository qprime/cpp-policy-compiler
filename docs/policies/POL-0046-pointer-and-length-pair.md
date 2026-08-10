---
id: POL-0046
kind: anti-pattern
replacement: [POL-0035]
attribution:
  - source: cpp-convention/conventions.md
    locator: "Trap: pointer-and-length pair"
    upstream: ["CG I.13"]
---

# Never pass a sequence as a pointer and a length

`(const T* data, std::size_t length)` puts the lifetime contract in a comment
and the bounds check on every caller. The two parameters are also adjacent and
independently wrong, so a stale length compiles.

```cpp
// Never: nothing ties the length to the pointer, and nothing ties either to a lifetime
Digest checksum(const std::uint8_t* data, std::size_t length);

// Instead: the sequence type carries its own bounds — POL-0035 per declared standard
Digest checksum(std::span<const std::uint8_t> bytes);
```

At an `extern "C"` boundary the foreign signature dictates the pair. Convert on
entry and never touch the raw pointer again.

```cpp
extern "C" int checksum_c(const std::uint8_t* data, std::size_t length) {
    const std::span<const std::uint8_t> bytes(data, length);
    // body uses bytes only
}
```

The pair is two facts that must agree, held by a language that will not check
that they do. Every caller re-derives the length, and a caller that re-derives it
from a stale variable produces an out-of-bounds read that is undefined rather
than diagnosed (POL-0019). Converting at the seam confines the disagreement to
one line, which is also the one line where the foreign contract is actually
known.
