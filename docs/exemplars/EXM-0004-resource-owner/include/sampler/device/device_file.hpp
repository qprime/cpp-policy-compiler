#ifndef SAMPLER_DEVICE_DEVICE_FILE_HPP
#define SAMPLER_DEVICE_DEVICE_FILE_HPP

#include <string>
#include <type_traits>

namespace sampler::device {

// POSIX descriptors are the platform dependency of this layer; nothing outside
// this type touches one.
class DeviceFile {
 public:
    explicit DeviceFile(const std::string& path);
    ~DeviceFile();

    DeviceFile(const DeviceFile&) = delete;
    DeviceFile& operator=(const DeviceFile&) = delete;
    DeviceFile(DeviceFile&& other) noexcept;
    DeviceFile& operator=(DeviceFile&& other) noexcept;

    int descriptor() const { return descriptor_; }

 private:
    int descriptor_;
};

static_assert(!std::is_copy_constructible_v<DeviceFile>);
static_assert(std::is_nothrow_move_constructible_v<DeviceFile>);

}  // namespace sampler::device

#endif  // SAMPLER_DEVICE_DEVICE_FILE_HPP
