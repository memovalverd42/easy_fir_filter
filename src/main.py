import numpy as np
from easy_fir_filter import EasyFirFilter, FilterConf
from easy_fir_filter.utils.table import show_coefficients_table

import matplotlib.pyplot as plt
from scipy.signal import freqz

from tests.filters.highpass_filter_tests import highpass_filter_configurations
from tests.filters.lowpass_filter_tests import lowpass_filter_configurations

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

# list_filter_configurations: list[FilterConf] = [
#     {
#         "filter_type": "highpass",
#         "window_type": "hamming",
#         "sampling_freq_hz": 80,
#         "passband_freq_hz": 16,
#         "stopband_freq_hz": 8,
#         "passband_ripple_db": 0.4,
#         "stopband_attenuation_db": 34,
#     },
#     {
#         "filter_type": "lowpass",
#         "window_type": "hamming",
#         "sampling_freq_hz": 2500,
#         "passband_freq_hz": 500,
#         "stopband_freq_hz": 750,
#         "passband_ripple_db": 0.1,
#         "stopband_attenuation_db": 44,
#     },
#     {
#         "filter_type": "highpass",
#         "window_type": "kaiser",
#         "sampling_freq_hz": 80,
#         "passband_freq_hz": 16,
#         "stopband_freq_hz": 8,
#         "passband_ripple_db": 0.3,
#         "stopband_attenuation_db": 35,
#     },
#     {
#         "filter_type": "bandstop",
#         "window_type": "kaiser",
#         "sampling_freq_hz": 13000,
#         "passband_freq_hz": 2000,
#         "stopband_freq_hz": 3000,
#         "passband_freq2_hz": 5000,
#         "stopband_freq2_hz": 4000,
#         "passband_ripple_db": 0.2,
#         "stopband_attenuation_db": 43,
#     },
#     {
#         "filter_type": "bandpass",
#         "window_type": "blackman",
#         "sampling_freq_hz": 80,
#         "passband_freq_hz": 16,
#         "stopband_freq_hz": 8,
#         "passband_freq2_hz": 24,
#         "stopband_freq2_hz": 32,
#         "passband_ripple_db": 0.4,
#         "stopband_attenuation_db": 34,
#     },
# ]

# filter = {
#     "filter_type": "highpass",
#     "window_type": "kaiser",
#     "sampling_freq_hz": 22050,
#     "stopband_freq_hz": 200,
#     "passband_freq_hz": 300,
#     "passband_ripple_db": 0.1,
#     "stopband_attenuation_db": 45,
# }
#
# my_filter = EasyFirFilter(
#     filter,
#     7,
# )
#
# coefficients = my_filter.calculate_filter()

for conf in highpass_filter_configurations:
    my_filter = EasyFirFilter(conf, 7)
    my_filter.calculate_delta()
    my_filter.calculate_ripples()
    d = my_filter.calculate_d_parameter()
    # print(d)
    order = my_filter.filter.calculate_filter_order(my_filter.D)
    # print(order)
    c = my_filter.filter.calculate_impulse_response_coefficients()
    print(c)

# print(len(my_filter.calculate_filter()))

# print(show_coefficients_table(coefficients))

# print(coefficients)

# b = np.array(coefficients)
# w, h = freqz(b, worN=8000)
#
# sampling_freq_hz = filter["sampling_freq_hz"]
# nyquist = sampling_freq_hz / 2
#
# # **Magnitud vs Frecuencia**
# plt.figure(figsize=(8, 5))
# plt.plot(w / np.pi * nyquist, np.abs(h))
# plt.title("Magnitud vs Frecuencia")
# plt.xlabel("Frecuencia (Hz)")
# plt.ylabel("Magnitud")
# plt.grid()
# plt.show()
#
# # **Log Magnitud vs Frecuencia**
# plt.figure(figsize=(8, 5))
# plt.plot(w / np.pi * nyquist, 20 * np.log10(np.abs(h)))
# plt.title("Log Magnitud vs Frecuencia")
# plt.xlabel("Frecuencia (Hz)")
# plt.ylabel("Magnitud (dB)")
# plt.grid()
# plt.show()
#
# import json
#
# # Convertir los datos a listas para que sean serializables en JSON
# freqs = (w / np.pi * nyquist).tolist()
# magnitudes = np.abs(h).tolist()
# log_magnitudes = (20 * np.log10(np.abs(h))).tolist()
#
# # Guardar en un archivo JSON
# data = {
#     "frequencies": freqs,
#     "magnitudes": magnitudes,
#     "log_magnitudes": log_magnitudes,
# }
#
# with open("filter_response.json", "w") as f:
#     json.dump(data, f, indent=4)
#
# print("Datos exportados a filter_response.json")
