#include "sampler/device/latest_reading.hpp"

#include <optional>
#include <thread>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"

namespace sampler::device {
namespace {

constexpr int kRounds = 10'000;
constexpr double kFirstWriterCelsius = 20.0;
constexpr double kSecondWriterCelsius = 21.0;

}  // namespace

TEST_CASE("reader_observes_the_last_written_value") {
    LatestReading cache;
    REQUIRE(cache.latest() == std::nullopt);

    cache.write_reading(core::Temperature{kFirstWriterCelsius});
    cache.write_reading(core::Temperature{kSecondWriterCelsius});

    REQUIRE(cache.latest() == core::Temperature{kSecondWriterCelsius});
}

TEST_CASE("two_writers_and_a_reader_complete_without_deadlock") {
    LatestReading cache;
    {
        const std::jthread first{[&cache] {
            for (int round = 0; round < kRounds; ++round) {
                cache.write_reading(core::Temperature{kFirstWriterCelsius});
            }
        }};
        const std::jthread second{[&cache] {
            for (int round = 0; round < kRounds; ++round) {
                cache.write_reading(core::Temperature{kSecondWriterCelsius});
            }
        }};
        const std::jthread reader{[&cache] {
            for (int round = 0; round < kRounds; ++round) {
                static_cast<void>(cache.latest());
            }
        }};
    }

    const std::optional<core::Temperature> settled = cache.latest();

    REQUIRE(settled.has_value());
    REQUIRE((settled == core::Temperature{kFirstWriterCelsius} ||
             settled == core::Temperature{kSecondWriterCelsius}));
}

}  // namespace sampler::device
