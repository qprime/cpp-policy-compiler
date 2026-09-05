#ifndef SAMPLER_DEVICE_ASYNC_READ_HPP
#define SAMPLER_DEVICE_ASYNC_READ_HPP

#include <coroutine>
#include <exception>
#include <memory>
#include <optional>

#include "sampler/core/temperature.hpp"

namespace sampler::device {

// Threading: a ReadSlot is single-threaded. The reader awaits it and the device
// writes to it from the same thread; a slot shared across threads would need a
// different type.
class ReadSlot {
 public:
    bool await_ready() const noexcept { return reading_.has_value(); }
    void await_suspend(std::coroutine_handle<> waiter) noexcept { waiter_ = waiter; }
    core::Temperature await_resume() const { return *reading_; }

    void write_reading(core::Temperature reading);
    void cancel(std::coroutine_handle<> waiter) noexcept;

 private:
    std::optional<core::Temperature> reading_;
    std::coroutine_handle<> waiter_;
};

class ReadTask {
 public:
    struct promise_type {
        explicit promise_type(std::shared_ptr<ReadSlot> slot, double) : slot{slot} {}

        std::optional<core::Temperature> reading;
        std::exception_ptr error;
        std::weak_ptr<ReadSlot> slot;

        ReadTask get_return_object();
        std::suspend_never initial_suspend() const noexcept { return {}; }
        std::suspend_always final_suspend() const noexcept { return {}; }
        void return_value(core::Temperature value) { reading = value; }
        void unhandled_exception() { error = std::current_exception(); }
    };

    explicit ReadTask(std::coroutine_handle<promise_type> handle) noexcept;
    ~ReadTask();

    ReadTask(const ReadTask&) = delete;
    ReadTask& operator=(const ReadTask&) = delete;
    ReadTask(ReadTask&& other) noexcept;
    ReadTask& operator=(ReadTask&& other) noexcept;

    bool is_done() const noexcept;
    core::Temperature get_reading() const;

 private:
    void cancel_wait() noexcept;

    std::coroutine_handle<promise_type> handle_;
};

ReadTask load_reading(std::shared_ptr<ReadSlot> slot, double offset_celsius);

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_ASYNC_READ_HPP
