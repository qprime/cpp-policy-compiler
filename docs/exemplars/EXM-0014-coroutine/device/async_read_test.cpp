#include "sampler/device/async_read.hpp"

#include <memory>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"

namespace sampler::device {
namespace {

constexpr double kOffsetCelsius = 1.5;

}  // namespace

TEST_CASE("resumes_with_the_read_value") {
    const std::shared_ptr<ReadSlot> slot = std::make_shared<ReadSlot>();
    const ReadTask task = load_reading(slot, kOffsetCelsius);
    REQUIRE_FALSE(task.is_done());

    slot->write_reading(core::Temperature{20.0});

    REQUIRE(task.is_done());
    REQUIRE(task.get_reading() == core::Temperature{21.5});
}

TEST_CASE("completes_without_suspending_when_the_reading_is_already_there") {
    const std::shared_ptr<ReadSlot> slot = std::make_shared<ReadSlot>();
    slot->write_reading(core::Temperature{20.0});

    const ReadTask task = load_reading(slot, kOffsetCelsius);

    REQUIRE(task.is_done());
    REQUIRE(task.get_reading() == core::Temperature{21.5});
}

TEST_CASE("the_slot_outlives_the_awaiting_coroutine") {
    std::weak_ptr<ReadSlot> observer;
    {
        const std::shared_ptr<ReadSlot> slot = std::make_shared<ReadSlot>();
        observer = slot;
        const ReadTask task = load_reading(slot, kOffsetCelsius);
        REQUIRE(observer.use_count() == 2);
    }

    REQUIRE(observer.expired());
}

TEST_CASE("destroying_an_unfinished_task_disconnects_its_continuation") {
    const std::shared_ptr<ReadSlot> slot = std::make_shared<ReadSlot>();
    {
        const ReadTask task = load_reading(slot, kOffsetCelsius);
        REQUIRE_FALSE(task.is_done());
    }

    slot->write_reading(core::Temperature{20.0});
}

}  // namespace sampler::device
