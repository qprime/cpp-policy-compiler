#include "sampler/core/log.hpp"

#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>

namespace sampler::core {
namespace {

std::string_view format_level(LogLevel level) {
    switch (level) {
        case LogLevel::Trace:
            return "TRACE";
        case LogLevel::Debug:
            return "DEBUG";
        case LogLevel::Info:
            return "INFO";
        case LogLevel::Warn:
            return "WARN";
        case LogLevel::Error:
            return "ERROR";
        case LogLevel::Fatal:
            return "FATAL";
    }
    throw std::logic_error("write_log: level must be a declared enumerator, got " +
                           std::to_string(static_cast<int>(level)));
}

}  // namespace

void write_log(LogLevel level, std::string_view message) {
    std::clog << format_level(level) << ' ' << message << '\n';
}

}  // namespace sampler::core
