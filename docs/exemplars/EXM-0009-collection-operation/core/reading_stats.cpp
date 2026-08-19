#include "sampler/core/reading_stats.hpp"

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
    if (lowest_celsius > highest_celsius) {
        throw std::invalid_argument(
            "SampleWindow: lowest_celsius must be <= highest_celsius, got " +
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

    const double total_celsius =
        std::accumulate(within_celsius.begin(), within_celsius.end(), 0.0);
    return Temperature{total_celsius / static_cast<double>(count)};
}

}  // namespace sampler::core
