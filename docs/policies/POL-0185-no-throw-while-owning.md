---
id: POL-0185
kind: standard
trigger: "throw while a resource is held"
attribution:
  - source: standard-practice
    locator: "exception safety"
    upstream: ["CG E.13"]
---

# Never throw while holding a resource that nothing will release

Give every resource to an owning object before anything that can throw. Then a
throw unwinds through destructors that release.

```cpp
auto port = std::make_unique<SerialPort>(device);
validate(job);                                // safe: port is owned
stream(*port, job);

SerialPort* port = new SerialPort(device);
validate(job);                                // throws: port leaks
```

Between the allocation and the moment an owner takes it, the resource belongs to
nobody, so an exception in that window leaks it with no way to recover. Getting the
ordering right is the same discipline as handing every allocation straight to a
manager.
