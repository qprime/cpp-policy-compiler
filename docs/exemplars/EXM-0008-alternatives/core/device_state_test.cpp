#include "sampler/core/device_state.hpp"

#include <chrono>

#include <catch2/catch_test_macros.hpp>

namespace sampler::core {

TEST_CASE("reports_offline_for_the_offline_alternative") {
    REQUIRE(state_to_health(Offline{}) == Health::Offline);
}

TEST_CASE("reports_healthy_for_both_running_alternatives") {
    REQUIRE(state_to_health(Idle{}) == Health::Healthy);
    REQUIRE(state_to_health(Sampling{std::chrono::milliseconds{250}}) == Health::Healthy);
}

TEST_CASE("reports_the_last_error_for_the_faulted_alternative") {
    REQUIRE(state_to_health(Faulted{"sensor timeout"}) == Health::Faulted);
    REQUIRE(format_state(Faulted{"sensor timeout"}) == "faulted: sensor timeout");
}

TEST_CASE("formats_the_period_of_a_sampling_state") {
    REQUIRE(format_state(Sampling{std::chrono::milliseconds{250}}) == "sampling every 250 ms");
}

TEST_CASE("formats_every_health_value") {
    REQUIRE(format_health(Health::Offline) == "offline");
    REQUIRE(format_health(Health::Healthy) == "healthy");
    REQUIRE(format_health(Health::Faulted) == "faulted");
}

}  // namespace sampler::core
