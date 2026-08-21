---
id: POL-0016
kind: standard
trigger: "reach for a singleton"
attribution:
  - source: standard-practice
    locator: "singletons"
    upstream: ["CG I.3"]
---

# A single instance is passed in, never reached for

When a program needs exactly one of something, construct it once at the top and
pass it down. Do not provide a static accessor that hands it to anyone who asks.

```cpp
int main() {
    MachineConfig config = load_machine_config(path);
    Planner planner(config);
    return run(planner);
}

MachineConfig& MachineConfig::instance();   // no
```

`instance()` makes the dependency invisible in every signature that uses it,
fixes the lifetime to program duration, and makes two configurations in one
process impossible — which is what a test needs first.
