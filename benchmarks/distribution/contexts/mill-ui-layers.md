# mill_ui C++ Layers

The native C++ tree is an implementation layer beneath the Python CAM system. Public
FFI functions translate and validate at the boundary. Domain code produces semantic
removal intent before planning chooses toolpaths. Code must not bypass that semantic
IR, and dependencies flow from the boundary through validated domain values toward
mechanism.
