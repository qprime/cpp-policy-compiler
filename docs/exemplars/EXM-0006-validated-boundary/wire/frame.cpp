#include "sampler/wire/frame.hpp"

#include <array>
#include <bit>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <expected>
#include <optional>
#include <span>

#include "sampler/core/temperature.hpp"

namespace sampler::wire {
namespace {

constexpr std::size_t kSequenceOffset = 0;
constexpr std::size_t kCelsiusOffset = 4;
constexpr std::size_t kWordSizeBytes = 4;
constexpr unsigned int kBitsPerByte = 8;

std::uint32_t read_word_be(std::span<const std::byte> bytes) {
    std::uint32_t word = 0;
    for (const std::byte octet : bytes.first(kWordSizeBytes)) {
        word = (word << kBitsPerByte) | std::to_integer<std::uint32_t>(octet);
    }
    return word;
}

void write_word_be(std::uint32_t word, std::span<std::byte> bytes) {
    for (std::size_t index = 0; index < kWordSizeBytes; ++index) {
        const unsigned int shift =
            static_cast<unsigned int>(kWordSizeBytes - 1 - index) * kBitsPerByte;
        bytes[index] = static_cast<std::byte>((word >> shift) & 0xFFu);
    }
}

}  // namespace

std::expected<Reading, DecodeError> parse_frame(std::span<const std::byte> frame) {
    if (frame.size() < kFrameSizeBytes) {
        return std::unexpected{DecodeError::TruncatedFrame};
    }

    const std::uint32_t sequence = read_word_be(frame.subspan(kSequenceOffset, kWordSizeBytes));
    const float celsius = std::bit_cast<float>(read_word_be(frame.subspan(kCelsiusOffset)));
    if (!std::isfinite(celsius)) {
        return std::unexpected{DecodeError::NotANumber};
    }

    const std::optional<core::Temperature> temperature = core::Temperature::try_from(celsius);
    if (!temperature.has_value()) {
        return std::unexpected{DecodeError::TemperatureOutOfRange};
    }
    return Reading{sequence, *temperature};
}

std::array<std::byte, kFrameSizeBytes> reading_to_frame(const Reading& reading) {
    std::array<std::byte, kFrameSizeBytes> frame{};
    write_word_be(reading.sequence, std::span{frame}.subspan(kSequenceOffset, kWordSizeBytes));
    write_word_be(std::bit_cast<std::uint32_t>(static_cast<float>(reading.temperature.celsius())),
                  std::span{frame}.subspan(kCelsiusOffset, kWordSizeBytes));
    return frame;
}

}  // namespace sampler::wire
