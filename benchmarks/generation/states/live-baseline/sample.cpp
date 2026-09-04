struct Result {
    int value;
};

Result make_result() {
    Result result{42};
    return result;
}

int* find_value(bool found) {
    static int value = 42;
    return found ? &value : nullptr;
}
