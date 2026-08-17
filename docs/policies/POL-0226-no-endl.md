---
id: POL-0226
kind: standard
attribution:
  - source: standard-practice
    locator: "stream flushing"
    upstream: ["CG SL.io.50", "CG SL.io.10"]
---

# Write `'\n'`; flush deliberately

Never `std::endl`. Where a flush matters — before a prompt, before a crash-prone
section — call `std::flush` and let the reader see that a flush was intended. Where a
program uses streams and not `printf`, call `std::ios_base::sync_with_stdio(false)`
once at start-up.

```cpp
int main() {
    std::ios_base::sync_with_stdio(false);
    std::cout << "planning\n";
    std::cout << "ready> " << std::flush;
}
```

`std::endl` writes a newline and flushes, so a loop using it forces a syscall per
line — often the whole cost of writing a large file. Keeping the flush separate makes
the flushes countable and intentional.
