from easy_fir_filter import EasyFirFilter, FilterConf

my_filter_conf: FilterConf = {
    "filter_type": "lowpass",
    "window_type": "blackman",
    "sampling_freq_hz": 140000,
    "passband_freq_hz": 40000,
    "stopband_freq_hz": 50000,
    "passband_ripple_db": 1,
    "stopband_attenuation_db": 40,
}

lowpass_filter = EasyFirFilter(my_filter_conf)

print(lowpass_filter)
