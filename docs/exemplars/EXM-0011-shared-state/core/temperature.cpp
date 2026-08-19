#include "sampler/core/temperature.hpp"

#include <optional>
#include <stdexcept>
#include <string>

namespace sampler::core {
namespace {

constexpr bool is_above_absolute_zero(double celsius) {
    return celsius >= kAbsoluteZeroCelsius;
}

}  // namespace

Temperature::Temperature(double celsius) : celsius_{celsius} {
    if (!is_above_absolute_zero(celsius)) {
        throw std::invalid_argument("Temperature: celsius must be >= -273.15, got " +
                                    std::to_string(celsius));
    }
}

std::optional<Temperature> Temperature::try_from(double celsius) {
    if (!is_above_absolute_zero(celsius)) {
        return std::nullopt;
    }
    return Temperature{celsius};
}

}  // namespace sampler::core
