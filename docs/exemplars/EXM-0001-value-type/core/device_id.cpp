#include "sampler/core/device_id.hpp"

#include <stdexcept>
#include <string>
#include <utility>

namespace sampler::core {

DeviceId::DeviceId(std::string text) : text_{std::move(text)} {
    if (text_.empty()) {
        throw std::invalid_argument("DeviceId: text must be non-empty, got \"\"");
    }
}

}  // namespace sampler::core
