#include <functional>
#include <mutex>
#include <utility>

struct Result {};

Result make_result() {
    Result result;
    return std::move(result);
}

const int* find_value(bool found) {
    if (!found) {
        return 0;
    }
    static const int value = 1;
    return &value;
}

void notify(std::mutex& mutex, const std::function<void()>& callback) {
    const std::lock_guard lock(mutex);
    callback();
}

int add(int left, int right) {
    return left + right;
}
