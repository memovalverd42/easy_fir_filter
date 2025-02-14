import numpy as np
from easy_fir_filter import EasyFirFilter, FilterConf

highpass_hamming_conf: FilterConf = {
    "filter_type": "highpass",
    "window_type": "hamming",
    "sampling_freq_hz": 80,
    "passband_freq_hz": 16,
    "stopband_freq_hz": 8,
    "passband_ripple_db": 0.4,
    "stopband_attenuation_db": 34,
}

lowpass_hamming_conf: FilterConf = {
    "filter_type": "lowpass",
    "window_type": "hamming",
    "sampling_freq_hz": 2500,
    "passband_freq_hz": 500,
    "stopband_freq_hz": 750,
    "passband_ripple_db": 0.1,
    "stopband_attenuation_db": 44,
}

highpass_kaiser_conf: FilterConf = {
    "filter_type": "highpass",
    "window_type": "kaiser",
    "sampling_freq_hz": 80,
    "passband_freq_hz": 16,
    "stopband_freq_hz": 8,
    "passband_ripple_db": 0.3,
    "stopband_attenuation_db": 35,
}

bandstop_kaiser_conf: FilterConf = {
    "filter_type": "bandstop",
    "window_type": "kaiser",
    "sampling_freq_hz": 13000,
    "passband_freq_hz": 2000,
    "stopband_freq_hz": 3000,
    "passband_freq2_hz": 5000,
    "stopband_freq2_hz": 4000,
    "passband_ripple_db": 0.2,
    "stopband_attenuation_db": 43,
}

bandpass_hamming_conf: FilterConf = {
    "filter_type": "bandpass",
    "window_type": "blackman",
    "sampling_freq_hz": 80,
    "passband_freq_hz": 16,
    "stopband_freq_hz": 8,
    "passband_freq2_hz": 24,
    "stopband_freq2_hz": 32,
    "passband_ripple_db": 0.4,
    "stopband_attenuation_db": 34,
}

my_filter = EasyFirFilter(bandpass_hamming_conf, 7)

coefficients = my_filter.calculate_filter()

print(coefficients)
