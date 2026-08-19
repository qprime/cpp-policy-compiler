#ifndef SAMPLER_CORE_LOG_HPP
#define SAMPLER_CORE_LOG_HPP

#include <string_view>

namespace sampler::core {

enum class LogLevel { Trace, Debug, Info, Warn, Error, Fatal };

void write_log(LogLevel level, std::string_view message);

}  // namespace sampler::core

#endif  // SAMPLER_CORE_LOG_HPP
