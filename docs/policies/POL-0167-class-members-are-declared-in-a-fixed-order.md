---
id: POL-0167
kind: standard
attribution:
  - source: standard-practice
    locator: "class member declaration order"
    upstream: ["CG NL.16"]
---

# A class declares its members in one order: public interface first, data last

```cpp
class ToolTable {
 public:
    static std::optional<ToolTable> try_load(const std::filesystem::path& path);

    std::optional<Tool> find(ToolId id) const;
    std::size_t size() const;

 protected:
    void invalidate();

 private:
    explicit ToolTable(std::vector<Tool> tools);

    std::unordered_map<ToolId, Tool> by_id_;
};
```

`public`, then `protected`, then `private`. Within each: types and aliases,
then constructors and the special members, then the operations, then data.

Data members go last and are `private` (POL-0126), and their relative order is
constrained by POL-0136 where one initializes from another.

A reader opening a class wants its interface, which is the public operations,
and almost never wants its representation first. Putting data at the top makes
every reader scroll past the part they were told not to depend on.

The order is fixed rather than chosen per class for the reason POL-0004 gives:
where two arrangements are equally correct, one arrangement everywhere means no
one spends attention on the question, and a class that departs from it is
signalling something rather than expressing a preference.
