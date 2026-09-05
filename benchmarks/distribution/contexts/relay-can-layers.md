# Relay CAN Layers

Task-spec YAML is the semantic input. Strategy modules validate and project neutral
communication bindings. The generator emits Structured Text, the Python simulator is
the behavioral oracle, and the C++ host independently executes and verifies the same
assertion contract. Transport implementations sit below the strategy-neutral host
surface; framework code does not branch on the CAN strategy name.
