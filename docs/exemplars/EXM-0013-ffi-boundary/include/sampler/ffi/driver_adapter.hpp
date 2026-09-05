#ifndef SAMPLER_FFI_DRIVER_ADAPTER_HPP
#define SAMPLER_FFI_DRIVER_ADAPTER_HPP

#include <cstdint>
#include <expected>
#include <stdexcept>
#include <string>

#include "sampler/core/temperature.hpp"
#include "sampler/ffi/driver.h"

// This layer converts foreign status codes and owns a foreign handle. The C
// provider validates its public pointer boundary; this trusted wrapper passes
// values whose stronger C++ contracts are already established.
namespace sampler::ffi {

enum class DriverFailure { NotFound, Busy, Fault };

class DriverError : public std::runtime_error {
 public:
    DriverError(DriverFailure failure, const std::string& message);

    DriverFailure failure() const noexcept { return failure_; }

 private:
    DriverFailure failure_;
};

DriverFailure status_to_failure(sampler_driver_status status);

class DriverSession {
 public:
    explicit DriverSession(const std::string& endpoint);
    ~DriverSession();

    DriverSession(const DriverSession&) = delete;
    DriverSession& operator=(const DriverSession&) = delete;
    DriverSession(DriverSession&& other) noexcept;
    DriverSession& operator=(DriverSession&& other) noexcept;

    std::expected<core::Temperature, DriverFailure> try_read() const;

 private:
    sampler_driver_session* session_;
};

std::string format_frame(std::uint32_t sequence, const core::Temperature& reading);

}  // namespace sampler::ffi

#endif  // SAMPLER_FFI_DRIVER_ADAPTER_HPP
