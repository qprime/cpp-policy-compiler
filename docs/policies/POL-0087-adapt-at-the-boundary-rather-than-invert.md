---
id: POL-0087
kind: standard
attribution:
  - source: cpp-convention/conventions.md
    locator: "Dependency Direction: a lower layer needs a higher layer's type"
---

# A lower layer that needs a higher layer's type gets an adapter

Where a lower layer needs something a higher layer knows, an adapter at the
boundary converts it into a type the lower layer already owns. The higher
layer's headers do not come down (POL-0018).

Three forms, in order of preference:

1. The lower layer declares the type it needs, and the higher layer supplies a
   value of it.
2. The lower layer takes a callback or an interface it declares, which the
   higher layer implements.
3. An adapter type at the boundary translates between the two.

The first is usually available and usually skipped, because pulling the existing
type down is one line and declaring a new one is several.

An include added to satisfy one call permanently attaches everything else that
header declares, and the attachment is invisible from the line that created it.
The lower layer then cannot be built, tested, or reused without the higher one,
which is the specific loss the direction rule exists to prevent. An adapter costs
a type and a conversion and confines the knowledge of both layers to one file,
which is also the file to change when either side moves.
