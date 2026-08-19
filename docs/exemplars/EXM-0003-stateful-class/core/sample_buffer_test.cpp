#include "sampler/core/sample_buffer.hpp"

#include <stdexcept>
#include <vector>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"

namespace sampler::core {

TEST_CASE("rejects_a_zero_capacity") {
    REQUIRE_THROWS_AS(SampleBuffer{0}, std::invalid_argument);
}

TEST_CASE("reports_full_only_at_capacity") {
    SampleBuffer buffer{2};
    REQUIRE(buffer.is_empty());

    buffer.push_back(Temperature{20.0});
    REQUIRE_FALSE(buffer.is_full());

    buffer.push_back(Temperature{21.0});
    REQUIRE(buffer.is_full());
}

TEST_CASE("drops_the_oldest_reading_when_full") {
    SampleBuffer buffer{2};
    buffer.push_back(Temperature{20.0});
    buffer.push_back(Temperature{21.0});
    buffer.push_back(Temperature{22.0});

    const std::vector<Temperature> expected{Temperature{21.0}, Temperature{22.0}};

    REQUIRE(buffer.size() == 2);
    REQUIRE(buffer.readings() == expected);
}

}  // namespace sampler::core
