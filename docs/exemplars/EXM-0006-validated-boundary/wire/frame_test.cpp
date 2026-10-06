#include "sampler/wire/frame.hpp"

#include <array>
#include <cstddef>
#include <expected>
#include <limits>
#include <span>

#include <catch2/catch_test_macros.hpp>

#include "sampler/core/temperature.hpp"

namespace sampler::wire {
namespace {

constexpr std::array<std::byte, kFrameSizeBytes> kRoomTemperatureFrame{
    std::byte{0x00}, std::byte{0x00}, std::byte{0x00}, std::byte{0x07},
    std::byte{0x41}, std::byte{0xA8}, std::byte{0x00}, std::byte{0x00},
};

constexpr std::array<std::byte, kFrameSizeBytes> kBelowAbsoluteZeroFrame{
    std::byte{0x00}, std::byte{0x00}, std::byte{0x00}, std::byte{0x07},
    std::byte{0xC3}, std::byte{0x96}, std::byte{0x00}, std::byte{0x00},
};

constexpr std::array<std::byte, kFrameSizeBytes> kNotANumberFrame{
    std::byte{0x00}, std::byte{0x00}, std::byte{0x00}, std::byte{0x07},
    std::byte{0x7F}, std::byte{0xC0}, std::byte{0x00}, std::byte{0x00},
};

}  // namespace

TEST_CASE("rejects_truncated_frame") {
    const std::array<std::byte, 3> truncated{std::byte{0x00}, std::byte{0x00}, std::byte{0x00}};

    const std::expected<Reading, DecodeError> decoded = parse_frame(truncated);

    REQUIRE_FALSE(decoded.has_value());
    REQUIRE(decoded.error() == DecodeError::TruncatedFrame);
}

TEST_CASE("rejects_out_of_range_temperature") {
    const std::expected<Reading, DecodeError> decoded = parse_frame(kBelowAbsoluteZeroFrame);

    REQUIRE_FALSE(decoded.has_value());
    REQUIRE(decoded.error() == DecodeError::TemperatureOutOfRange);
}

TEST_CASE("rejects_a_not_a_number_temperature") {
    const std::expected<Reading, DecodeError> decoded = parse_frame(kNotANumberFrame);

    REQUIRE_FALSE(decoded.has_value());
    REQUIRE(decoded.error() == DecodeError::NotANumber);
}

TEST_CASE("decodes_sequence_and_temperature") {
    const std::expected<Reading, DecodeError> decoded = parse_frame(kRoomTemperatureFrame);

    REQUIRE(decoded.has_value());
    REQUIRE(decoded->sequence == 7);
    REQUIRE(decoded->temperature == core::Temperature{21.0});
}

TEST_CASE("round_trips_semantically") {
    const std::expected<Reading, DecodeError> first = parse_frame(kRoomTemperatureFrame);
    REQUIRE(first.has_value());

    const auto encoded = reading_to_frame(*first);
    REQUIRE(encoded.has_value());
    const std::expected<Reading, DecodeError> second = parse_frame(*encoded);

    REQUIRE(second.has_value());
    REQUIRE(second->sequence == first->sequence);
    REQUIRE(second->temperature == first->temperature);
}

TEST_CASE("rejects_temperature_outside_the_wire_numeric_range") {
    const Reading reading{7, core::Temperature{std::numeric_limits<double>::max()}};
    const auto encoded = reading_to_frame(reading);
    REQUIRE_FALSE(encoded.has_value());
    REQUIRE(encoded.error() == EncodeError::TemperatureOutOfRange);
}

TEST_CASE("encodes_the_largest_finite_wire_temperature") {
    const Reading reading{7, core::Temperature{std::numeric_limits<float>::max()}};
    const auto encoded = reading_to_frame(reading);
    REQUIRE(encoded.has_value());
    const auto decoded = parse_frame(*encoded);
    REQUIRE(decoded.has_value());
    REQUIRE(decoded->temperature == reading.temperature);
}

}  // namespace sampler::wire
