#ifndef SAMPLER_WIRE_FRAME_HPP
#define SAMPLER_WIRE_FRAME_HPP

#include <array>
#include <cstddef>
#include <cstdint>
#include <expected>
#include <span>

#include "sampler/core/temperature.hpp"

namespace sampler::wire {

constexpr std::size_t kFrameSizeBytes = 8;

enum class DecodeError { TruncatedFrame, NotANumber, TemperatureOutOfRange };

struct Reading {
    std::uint32_t sequence;
    core::Temperature temperature;
};

std::expected<Reading, DecodeError> parse_frame(std::span<const std::byte> frame);

std::array<std::byte, kFrameSizeBytes> reading_to_frame(const Reading& reading);

}  // namespace sampler::wire

#endif  // SAMPLER_WIRE_FRAME_HPP
