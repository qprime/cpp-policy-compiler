#ifndef SAMPLER_FFI_DRIVER_H
#define SAMPLER_FFI_DRIVER_H

#ifdef __cplusplus
extern "C" {
#endif

typedef enum sampler_driver_status {
    SAMPLER_DRIVER_OK = 0,
    SAMPLER_DRIVER_NOT_FOUND = 1,
    SAMPLER_DRIVER_BUSY = 2,
    SAMPLER_DRIVER_FAULT = 3
} sampler_driver_status;

typedef struct sampler_driver_session sampler_driver_session;

sampler_driver_status sampler_driver_open(const char* endpoint,
                                          sampler_driver_session** out_session);

void sampler_driver_close(sampler_driver_session* session);

sampler_driver_status sampler_driver_read(sampler_driver_session* session, double* out_celsius);

#ifdef __cplusplus
}  // extern "C"
#endif

#endif  // SAMPLER_FFI_DRIVER_H
