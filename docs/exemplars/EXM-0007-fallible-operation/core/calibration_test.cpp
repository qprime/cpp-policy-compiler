#include "sampler/core/calibration.hpp"

#include <array>
#include <optional>
#include <stdexcept>

#include <catch2/catch_approx.hpp>
#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"

namespace sampler::core {

TEST_CASE("reports_domain_failure_for_unstable_input") {
    const Calibration calibration{2.0, 1.5};
    const std::array<double, 3> drifting{20.0, 25.0, 19.9};

    REQUIRE(try_calibrated_temperature(drifting, calibration) == std::nullopt);
}

TEST_CASE("precondition_violation_is_not_a_return_value") {
    REQUIRE_THROWS_AS(Calibration(2.0, 0.0), std::invalid_argument);
}

TEST_CASE("catches_a_plausible_wrong_implementation") {
    const Calibration calibration{2.0, 1.5};
    const std::array<double, 3> steady{20.0, 20.1, 19.9};

    const std::optional<Temperature> calibrated = try_calibrated_temperature(steady, calibration);

    REQUIRE(calibrated.has_value());
    REQUIRE(calibrated->celsius() == Catch::Approx(32.0));
}

}  // namespace sampler::core
