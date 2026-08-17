---
id: POL-0130
kind: standard
attribution:
  - source: standard-practice
    locator: "template mechanics"
    upstream: ["CG T.42", "CG T.43", "CG T.44", "CG T.60", "CG T.69", "CG T.143"]
---

# A template names its aliases with `using` and qualifies its calls

```cpp
// Never. typedef cannot be parameterized, and the unqualified call is a hook
// any caller's namespace can hijack.
template <typename T>
void emit(const T& value) { write(value); }

// Right.
template <typename T>
using Handle = std::unique_ptr<T, Release>;

template <typename T>
void emit(const T& value) { proj::io::write(value); }
```

Every non-member call inside a template is qualified, unless the call is a
deliberate customization point — and then it is opted into with a `using`
declaration in the template's own scope, so the extension is visible where it is
allowed rather than wherever a caller happens to define a name.

A template depends on as little of its surrounding context as it can. Deduce
class template arguments from a function template where that removes a
redundant type name.

Beware code that is generic only by accident: a template body calling a concrete
type's member, or assuming `int`, compiles for the one argument it was tested
with and fails for the second. Constraining the parameter (POL-0129) is what
turns that into a diagnostic at the declaration.

Unqualified lookup inside a template resolves partly at instantiation, in the
caller's namespace, so a function nobody in this file can see may be selected.
That makes the template's behaviour depend on where it is used, which defeats
POL-0007 and makes the failure impossible to reproduce from the template alone.
