from easy_fir_filter import EasyFirFilter, FilterConf

my_filter_conf: FilterConf = {
    "filter_type": "lowpass",
    "window_type": "hamming",
    "sampling_freq_hz": 80,
    "passband_freq_hz": 10,
    "stopband_freq_hz": 20,
    "passband_ripple_db": 1,
    "stopband_attenuation_db": 60,
}

print(my_filter_conf)

lowpass_filter = EasyFirFilter(my_filter_conf)

print(lowpass_filter)
