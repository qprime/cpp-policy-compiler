#include "sampler/device/sample_channel.hpp"

#include <chrono>
#include <optional>
#include <stdexcept>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"

namespace sampler::device {
namespace {

constexpr std::chrono::milliseconds kPopTimeout{200};

}  // namespace

TEST_CASE("rejects_a_zero_capacity") {
    REQUIRE_THROWS_AS(SampleChannel{0}, std::invalid_argument);
}

TEST_CASE("pops_what_was_pushed_in_order") {
    SampleChannel channel{2};

    REQUIRE(channel.try_push(core::Temperature{20.0}));
    REQUIRE(channel.try_push(core::Temperature{21.0}));

    REQUIRE(channel.try_pop(kPopTimeout) == core::Temperature{20.0});
    REQUIRE(channel.try_pop(kPopTimeout) == core::Temperature{21.0});
}

TEST_CASE("refuses_a_push_into_a_full_channel") {
    SampleChannel channel{1};
    REQUIRE(channel.try_push(core::Temperature{20.0}));

    REQUIRE_FALSE(channel.try_push(core::Temperature{21.0}));
}

TEST_CASE("reports_absence_when_the_wait_times_out") {
    SampleChannel channel{1};

    REQUIRE(channel.try_pop(std::chrono::milliseconds{1}) == std::nullopt);
}

}  // namespace sampler::device
