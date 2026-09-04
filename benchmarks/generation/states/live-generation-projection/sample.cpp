struct Result {
    int value;
    bool found;
};

Result make_result() {
    Result result;
    result.value = 42;
    result.found = true;
    return result;
}

int* find_value(bool found) {
    static int persistent_value = 42;
    return found ? &persistent_value : nullptr;
}
