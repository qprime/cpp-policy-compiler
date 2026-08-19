#include "sampler/core/sample_interval.hpp"

#include <chrono>
#include <stdexcept>

#include <catch2/catch_approx.hpp>
#include <catch2/catch_test_macros.hpp>

namespace sampler::core {

TEST_CASE("rejects_a_non_positive_period") {
    REQUIRE_THROWS_AS(SampleInterval{std::chrono::milliseconds{0}}, std::invalid_argument);
    REQUIRE_THROWS_AS(SampleInterval{std::chrono::milliseconds{-1}}, std::invalid_argument);
}

TEST_CASE("reports_the_rate_the_period_implies") {
    const SampleInterval interval{std::chrono::milliseconds{250}};

    REQUIRE(interval.rate_hz() == Catch::Approx(4.0));
}

}  // namespace sampler::core
