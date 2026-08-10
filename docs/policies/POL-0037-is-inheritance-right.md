---
id: POL-0037
kind: guideline
attribution:
  - source: cpp-convention/conventions.md
    locator: "Decision: is inheritance right"
    upstream: ["CG I.25", "CG C.35", "CG C.82", "CG C.128", "CG C.129"]
---

# Is inheritance right

Almost always no. Inheritance shares *implementation*, and implementation
sharing is not how variation is represented.

| Question | Answer |
|----------|--------|
| Is this a fixed set of alternatives? | Not inheritance. Closed-set variation (POL-0033) |
| Is it an open set of behaviours, injected by a caller? | An abstract interface with no data |
| Is it code reuse? | Not inheritance. Composition, or a free function (POL-0029) |
| Do I have at least two concrete cases in hand? | If not, write the function. Decide on the second |

Where a hierarchy is genuinely right, three rules travel with it: a polymorphic
base class has a public virtual destructor or a protected non-virtual one; a
virtual function specifies exactly one of `virtual`, `override`, `final`; and no
virtual function is called from a constructor or a destructor.

Inheritance answers two unrelated questions at once — what the values are and
where the code lives — and binds the answers together permanently. Once a
hierarchy exists, adding an alternative is easy and adding an operation touches
every class, which is the opposite of the trade a closed set of alternatives
wants. The compiler also stops helping: nothing reports that a derived class
failed to handle something, because from the language's view nothing is missing.
