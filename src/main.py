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

highpass_hamming = EasyFirFilter(highpass_hamming_conf)

coefficients = highpass_hamming.calculate_filter()
print(coefficients)


def is_symmetric(coeffs: list[float], tol=1e-6):
    return np.allclose(coeffs, coeffs[::-1], atol=tol)


h = np.array(coefficients)
print("Es simétrico:", is_symmetric(h))
