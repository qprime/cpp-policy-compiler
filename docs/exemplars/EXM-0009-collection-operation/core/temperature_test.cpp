#include "sampler/core/temperature.hpp"

#include <optional>
#include <stdexcept>

#include <catch2/catch_approx.hpp>
#include <catch2/catch_test_macros.hpp>

namespace sampler::core {

TEST_CASE("constructs_from_valid_celsius") {
    const Temperature reading{21.5};

    REQUIRE(reading.celsius() == 21.5);
    REQUIRE(reading.kelvin() == Catch::Approx(294.65));
}

TEST_CASE("rejects_below_absolute_zero") {
    REQUIRE_THROWS_AS(Temperature{-300.0}, std::invalid_argument);
}

TEST_CASE("try_from_reports_absence_below_absolute_zero") {
    REQUIRE(Temperature::try_from(-300.0) == std::nullopt);
    REQUIRE(Temperature::try_from(kAbsoluteZeroCelsius).has_value());
}

TEST_CASE("compares_equal_by_value") {
    REQUIRE(Temperature{21.5} == Temperature{21.5});
    REQUIRE(Temperature{21.5} != Temperature{21.6});
}

}  // namespace sampler::core
