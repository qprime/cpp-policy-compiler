#include "sampler/device/async_read.hpp"

#include <cassert>
#include <coroutine>
#include <exception>
#include <memory>
#include <utility>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

void ReadSlot::write_reading(core::Temperature reading) {
    reading_ = reading;
    if (waiter_) {
        const std::coroutine_handle<> waiter = std::exchange(waiter_, {});
        waiter.resume();
    }
}

ReadTask ReadTask::promise_type::get_return_object() {
    return ReadTask{std::coroutine_handle<promise_type>::from_promise(*this)};
}

ReadTask::ReadTask(std::coroutine_handle<promise_type> handle) noexcept : handle_{handle} {}

ReadTask::~ReadTask() {
    if (handle_) {
        handle_.destroy();
    }
}

ReadTask::ReadTask(ReadTask&& other) noexcept : handle_{std::exchange(other.handle_, {})} {}

ReadTask& ReadTask::operator=(ReadTask&& other) noexcept {
    if (this == &other) {
        return *this;
    }
    if (handle_) {
        handle_.destroy();
    }
    handle_ = std::exchange(other.handle_, {});
    return *this;
}

bool ReadTask::is_done() const noexcept { return handle_ && handle_.done(); }

core::Temperature ReadTask::get_reading() const {
    assert(is_done());

    const promise_type& promise = handle_.promise();
    if (promise.error) {
        std::rethrow_exception(promise.error);
    }
    return *promise.reading;
}

ReadTask load_reading(std::shared_ptr<ReadSlot> slot, double offset_celsius) {
    const core::Temperature raw = co_await *slot;
    co_return core::Temperature{raw.celsius() + offset_celsius};
}

}  // namespace sampler::device
