"""
This module contains a list of filter configurations that are used in the tests.
"""

from easy_fir_filter import FilterConf

list_filter_configurations: list[FilterConf] = [
    {
        "filter_type": "highpass",
        "window_type": "hamming",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 34,
    },
    {
        "filter_type": "lowpass",
        "window_type": "hamming",
        "sampling_freq_hz": 2500,
        "passband_freq_hz": 500,
        "stopband_freq_hz": 750,
        "passband_ripple_db": 0.1,
        "stopband_attenuation_db": 44,
    },
    {
        "filter_type": "highpass",
        "window_type": "kaiser",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_ripple_db": 0.3,
        "stopband_attenuation_db": 35,
    },
    {
        "filter_type": "bandstop",
        "window_type": "kaiser",
        "sampling_freq_hz": 13000,
        "passband_freq_hz": 2000,
        "stopband_freq_hz": 3000,
        "passband_freq2_hz": 5000,
        "stopband_freq2_hz": 4000,
        "passband_ripple_db": 0.2,
        "stopband_attenuation_db": 43,
    },
    {
        "filter_type": "bandpass",
        "window_type": "blackman",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_freq2_hz": 24,
        "stopband_freq2_hz": 32,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 34,
    },
]


delta_results = [
    0.0199526,
    0.0057563,
    0.0172676,
    0.0070794,
    0.0199526,
]

ripples_results = [
    (34.00001, 0.3466581),
    (44.7971316, 0.0999982),
    (35.2553604, 0.2999987),
    (43.0000709, 0.1229838),
    (34.00001, 0.3466581),
]

d_results = [
    1.8140675,
    2.5659562,
    1.9014874,
    2.4408127,
    1.8140675,
]

filter_length_results = [
    19,
    26,
    20,
    32,
    20,
]
