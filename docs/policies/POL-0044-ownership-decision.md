---
id: POL-0044
kind: pattern
trigger: "decide what type holds an object you allocate"
attribution:
  - source: cpp-convention/conventions.md
    locator: "Pattern: ownership decision"
    upstream: ["CG F.26", "CG F.27", "CG R.5", "CG R.20", "CG R.21", "CG ES.24"]
---

# Answer the ownership question in order and stop at the first yes

| Question | Answer |
|----------|--------|
| Does this need to outlive the current scope? | **No** → a value or an automatic variable. Do not heap-allocate. |
| Is there exactly one owner? | **Yes** → `std::unique_ptr<T>`, transferred by move |
| Are there genuinely multiple independent owners with no primary? | **Yes** → `std::shared_ptr<T>` |
| None of the above — you only need to look at it | `const T&`, or `T*` if null is meaningful |

```cpp
Toolpath path = plan_pocket(face, params);              // value: most code stops here
std::vector<Move> moves;                                // owned sequence
std::unique_ptr<PostProcessor> post = make_post(dialect);  // one owner, polymorphic
```

Most code never reaches question two. A value member, a `std::vector<T>`, and a
`const&` parameter cover the large majority of real ownership needs, and they are
the forms with no lifetime question left to answer.
