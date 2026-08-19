#include "sampler/ffi/driver_adapter.hpp"

#include <cstdint>
#include <expected>
#include <format>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>

#include "sampler/core/temperature.hpp"
#include "sampler/ffi/driver.h"

namespace sampler::ffi {
namespace {

constexpr int kCelsiusDecimals = 3;

std::string_view format_failure(DriverFailure failure) {
    switch (failure) {
        case DriverFailure::NotFound:
            return "not found";
        case DriverFailure::Busy:
            return "busy";
        case DriverFailure::Fault:
            return "fault";
    }
    throw std::logic_error("DriverError: failure must be a declared enumerator, got " +
                           std::to_string(static_cast<int>(failure)));
}

}  // namespace

DriverError::DriverError(DriverFailure failure, const std::string& message)
    : std::runtime_error{message}, failure_{failure} {}

DriverFailure status_to_failure(sampler_driver_status status) {
    switch (status) {
        case SAMPLER_DRIVER_NOT_FOUND:
            return DriverFailure::NotFound;
        case SAMPLER_DRIVER_BUSY:
            return DriverFailure::Busy;
        case SAMPLER_DRIVER_FAULT:
            return DriverFailure::Fault;
        case SAMPLER_DRIVER_OK:
            break;
    }
    throw std::logic_error("status_to_failure: status must name a failure, got " +
                           std::to_string(static_cast<int>(status)));
}

DriverSession::DriverSession(const std::string& endpoint) : session_{nullptr} {
    const sampler_driver_status status = sampler_driver_open(endpoint.c_str(), &session_);
    if (status != SAMPLER_DRIVER_OK) {
        const DriverFailure failure = status_to_failure(status);
        throw DriverError{failure, "DriverSession: endpoint must be openable, got \"" + endpoint +
                                       "\": " + std::string{format_failure(failure)}};
    }
}

DriverSession::~DriverSession() {
    if (session_ != nullptr) {
        sampler_driver_close(session_);
    }
}

DriverSession::DriverSession(DriverSession&& other) noexcept
    : session_{std::exchange(other.session_, nullptr)} {}

DriverSession& DriverSession::operator=(DriverSession&& other) noexcept {
    if (this == &other) {
        return *this;
    }
    if (session_ != nullptr) {
        sampler_driver_close(session_);
    }
    session_ = std::exchange(other.session_, nullptr);
    return *this;
}

std::expected<core::Temperature, DriverFailure> DriverSession::try_read() const {
    double celsius = 0.0;
    const sampler_driver_status status = sampler_driver_read(session_, &celsius);
    if (status != SAMPLER_DRIVER_OK) {
        return std::unexpected{status_to_failure(status)};
    }

    const std::optional<core::Temperature> reading = core::Temperature::try_from(celsius);
    if (!reading.has_value()) {
        return std::unexpected{DriverFailure::Fault};
    }
    return *reading;
}

std::string format_frame(std::uint32_t sequence, const core::Temperature& reading) {
    return std::format("{{\"sequence\":{},\"celsius\":{:.{}f}}}", sequence, reading.celsius(),
                       kCelsiusDecimals);
}

}  // namespace sampler::ffi
