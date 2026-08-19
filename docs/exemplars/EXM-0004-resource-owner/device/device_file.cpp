#include "sampler/device/device_file.hpp"

#include <cerrno>
#include <cstring>
#include <stdexcept>
#include <string>
#include <utility>

#include <fcntl.h>
#include <unistd.h>

namespace sampler::device {
namespace {

constexpr int kNoDescriptor = -1;

}  // namespace

DeviceFile::DeviceFile(const std::string& path)
    : descriptor_{::open(path.c_str(), O_RDONLY | O_CLOEXEC)} {
    if (descriptor_ == kNoDescriptor) {
        throw std::runtime_error("DeviceFile: path must name an openable device, got \"" + path +
                                 "\": " + std::strerror(errno));
    }
}

DeviceFile::~DeviceFile() {
    if (descriptor_ != kNoDescriptor) {
        ::close(descriptor_);
    }
}

DeviceFile::DeviceFile(DeviceFile&& other) noexcept
    : descriptor_{std::exchange(other.descriptor_, kNoDescriptor)} {}

DeviceFile& DeviceFile::operator=(DeviceFile&& other) noexcept {
    if (this == &other) {
        return *this;
    }
    if (descriptor_ != kNoDescriptor) {
        ::close(descriptor_);
    }
    descriptor_ = std::exchange(other.descriptor_, kNoDescriptor);
    return *this;
}

}  // namespace sampler::device
