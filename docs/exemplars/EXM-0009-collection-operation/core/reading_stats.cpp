#include "sampler/core/reading_stats.hpp"

#include <cmath>
#include <cstddef>
#include <iterator>
#include <numeric>
#include <optional>
#include <ranges>
#include <span>
#include <stdexcept>
#include <string>

#include "sampler/core/temperature.hpp"

namespace sampler::core {

SampleWindow::SampleWindow(double lowest_celsius, double highest_celsius)
    : lowest_celsius_{lowest_celsius}, highest_celsius_{highest_celsius} {
    if (!std::isfinite(lowest_celsius) || !std::isfinite(highest_celsius) ||
        lowest_celsius > highest_celsius) {
        throw std::invalid_argument(
            "SampleWindow: finite bounds must satisfy lowest_celsius <= highest_celsius, got " +
            std::to_string(lowest_celsius));
    }
}

std::optional<Temperature> try_mean_temperature(std::span<const Temperature> readings,
                                                const SampleWindow& window) {
    auto within_celsius =
        readings |
        std::views::transform([](const Temperature& reading) { return reading.celsius(); }) |
        std::views::filter([&window](double celsius) { return window.contains(celsius); });

    const auto count = std::ranges::distance(within_celsius);
    if (count == 0) {
        return std::nullopt;
    }

    std::size_t processed = 0;
    const double mean_celsius = std::accumulate(
        within_celsius.begin(), within_celsius.end(), 0.0,
        [&processed](double mean, double next) {
            ++processed;
            return std::lerp(mean, next, 1.0 / static_cast<double>(processed));
        });
    return Temperature{mean_celsius};
}

}  // namespace sampler::core
