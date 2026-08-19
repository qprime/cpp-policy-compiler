#include "sampler/device/poller.hpp"

#include <atomic>
#include <chrono>
#include <memory>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/sample_interval.hpp"

namespace sampler::device {
namespace {

constexpr std::chrono::milliseconds kFastPeriod{5};
constexpr std::chrono::milliseconds kPopTimeout{2000};

core::SampleInterval make_fast_interval() { return core::SampleInterval{kFastPeriod}; }

}  // namespace

TEST_CASE("stops_on_request") {
    Poller poller{make_fast_interval()};

    poller.stop();

    REQUIRE(poller.exit_flag()->load());
}

TEST_CASE("destructor_joins_the_running_thread") {
    std::shared_ptr<const std::atomic<bool>> exited;
    {
        Poller poller{make_fast_interval()};
        exited = poller.exit_flag();
        REQUIRE_FALSE(exited->load());
    }

    REQUIRE(exited->load());
}

TEST_CASE("writes_samples_into_its_own_channel") {
    Poller poller{make_fast_interval()};

    REQUIRE(poller.channel().try_pop(kPopTimeout).has_value());

    poller.stop();
}

}  // namespace sampler::device
