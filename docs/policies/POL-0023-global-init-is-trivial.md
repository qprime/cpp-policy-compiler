---
id: POL-0023
kind: standard
trigger: "declare an object at namespace scope"
attribution:
  - source: standard-practice
    locator: "static initialization order"
    upstream: ["CG I.22"]
---

# Namespace-scope objects are constant-initialized or they are not there

A namespace-scope object is `constexpr`, or `const` with a constant initializer.
Anything needing work at startup — reading a file, allocating, calling another
translation unit — is built inside `main` and passed down.

```cpp
constexpr double kMinMarginMm = 10.0;                      // fine
const MachineConfig kDefaults = load_config("defaults");    // no

int main() {
    const MachineConfig defaults = load_config("defaults");  // instead
    ...
}
```

Initialization order across translation units is unspecified, so a global that
calls into another translation unit either works by accident or fails by link
order. Startup failures there also happen before `main` can report them.
