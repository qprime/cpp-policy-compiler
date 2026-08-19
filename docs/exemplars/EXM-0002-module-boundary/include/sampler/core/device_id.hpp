#ifndef SAMPLER_CORE_DEVICE_ID_HPP
#define SAMPLER_CORE_DEVICE_ID_HPP

#include <compare>
#include <string>
#include <string_view>

namespace sampler::core {

class DeviceId {
 public:
    explicit DeviceId(std::string text);

    std::string_view text() const { return text_; }

    friend bool operator==(const DeviceId&, const DeviceId&) = default;
    friend std::strong_ordering operator<=>(const DeviceId&, const DeviceId&) = default;

 private:
    std::string text_;
};

}  // namespace sampler::core

#endif  // SAMPLER_CORE_DEVICE_ID_HPP
