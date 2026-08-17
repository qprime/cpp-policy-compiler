---
id: POL-0154
kind: anti-pattern
replacement: [POL-0129, POL-0117]
attribution:
  - source: standard-practice
    locator: "C mechanisms with C++ replacements"
    upstream: ["CG ES.34", "CG F.55", "CG Type.8", "CG SL.C.1"]
---

# Never write a C-style variadic function, `va_arg`, `setjmp`, or `longjmp`

```cpp
// Never. No type checking, no argument count, undefined behaviour on a mismatch.
void log_fmt(const char* fmt, ...);

// Right. A constrained variadic template, or std::format at the call site.
template <typename... Args>
void log_fmt(std::format_string<Args...> fmt, Args&&... args);

// Never. Jumps past destructors; every object in between leaks.
if (setjmp(recovery_) != 0) { return -1; }
```

A variadic template is type-checked and knows its argument count; `std::format`
covers the message-building case that produced most `printf`-style signatures
(POL-0111).

`longjmp` unwinds nothing. Destructors between the jump and the landing point do
not run, so every resource held across it leaks and every invariant established
by a constructor is silently abandoned — which is the guarantee POL-0003 rests
on, removed. Error propagation is a return type or an exception (POL-0031).

`va_arg` reads whatever bytes are at the next argument position and interprets
them as the requested type. A caller that passes an `int` where `long` is read
produces a garbage value with no diagnostic at either end, which is the class
POL-0008 exists to hand to the compiler instead.
