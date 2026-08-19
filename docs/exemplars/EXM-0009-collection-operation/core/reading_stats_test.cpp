#include "sampler/core/reading_stats.hpp"

#include <optional>
#include <stdexcept>
#include <vector>

#include <catch2/catch_approx.hpp>
#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators.hpp>

#include "sampler/core/temperature.hpp"

namespace sampler::core {
namespace {

struct RoomWindow {
    SampleWindow window{18.0, 24.0};
};

}  // namespace

TEST_CASE("rejects_an_inverted_window") {
    REQUIRE_THROWS_AS(SampleWindow(24.0, 18.0), std::invalid_argument);
}

TEST_CASE_METHOD(RoomWindow, "mean_of_empty_range_is_absent") {
    const std::vector<Temperature> readings =
        GENERATE(std::vector<Temperature>{},
                 std::vector<Temperature>{Temperature{5.0}},
                 std::vector<Temperature>{Temperature{40.0}, Temperature{-10.0}});

    REQUIRE(try_mean_temperature(readings, window) == std::nullopt);
}

TEST_CASE_METHOD(RoomWindow, "filters_before_reducing") {
    const std::vector<Temperature> readings{Temperature{20.0}, Temperature{100.0},
                                            Temperature{22.0}};

    const std::optional<Temperature> mean = try_mean_temperature(readings, window);

    REQUIRE(mean.has_value());
    REQUIRE(mean->celsius() == Catch::Approx(21.0));
}

}  // namespace sampler::core
