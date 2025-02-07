"""
This file contains the FilterConfValuesValidator class, which is used to validate the values of the filter configuration
"""

from typing import Literal

from easy_fir_filter.types.fir_filter_conf import FilterConf

_KEYS_LITERAL = Literal[
    "filter_type",
    "window_type",
    "passband_ripple_db",
    "stopband_attenuation_db",
    "passband_freq_hz",
    "stopband_freq_hz",
    "sampling_freq_hz",
    "stopband_freq2_hz",
    "passband_freq2_hz",
]


class _FilterConfValuesValidator:
    """
    This class is used to validate the values of the filter configuration
    """

    def __init__(self, filter_conf: FilterConf):
        self.filter_conf = filter_conf
        self._validate_values()

    def _extract_frequencies(self):
        """
        Extracts the frequencies from the filter configuration
        """
        return (
            self.filter_conf.get("passband_freq_hz"),
            self.filter_conf.get("passband_freq2_hz"),
            self.filter_conf.get("stopband_freq_hz"),
            self.filter_conf.get("stopband_freq2_hz"),
            self.filter_conf["sampling_freq_hz"],
        )

    def _validate_values(self):
        """
        Runs all necessary validations.
        """
        self._validate_ripples()
        self._validate_frequency_values()
        self._validate_frequencies_by_filter_type()

    def _validate_frequencies_grater_than(
        self, keys: list[_KEYS_LITERAL], value: int | float
    ):
        """
        Ensures specified frequencies are greater than a given value.
        """
        invalid_frequency = [
            key
            for key in keys
            if self.filter_conf[key] is not None and self.filter_conf[key] <= value
        ]
        if invalid_frequency:
            raise ValueError(
                f'{", ".join(invalid_frequency)} must be greater than {value}'
            )

    def _validate_frequencies_less_than(
        self, keys: list[_KEYS_LITERAL], value: int | float
    ):
        """
        Ensures specified frequencies are less than or equal to a given value.
        """
        invalid_frequency = [
            key
            for key in keys
            if self.filter_conf[key] is not None
            and self.filter_conf[key] > value  # 👈 Cambiado
        ]
        if invalid_frequency:
            raise ValueError(
                f'{", ".join(invalid_frequency)} must be less than or equal to {value}'
            )

    def _validate_ripples(self):
        """
        Validates the ripples.
        """
        passband_ripple = self.filter_conf["passband_ripple_db"]
        stopband_attenuation = self.filter_conf["stopband_attenuation_db"]

        if passband_ripple <= 0:
            raise ValueError("Passband ripple must be positive")

        if stopband_attenuation <= 0:
            raise ValueError("Stopband attenuation must be positive")

        if passband_ripple >= stopband_attenuation:
            raise ValueError("Passband ripple must be less than stopband attenuation")

    def _validate_frequencies_by_filter_type(self):
        """
        Validates the frequency order based on filter type.
        """
        filter_type = self.filter_conf["filter_type"]
        fp1, fp2, fs1, fs2, _ = self._extract_frequencies()

        if filter_type == "lowpass" and fp1 >= fs1:
            raise ValueError("For lowpass filter, fp1 must be less than fs1.")

        elif filter_type == "highpass" and fp1 <= fs1:
            raise ValueError("For highpass filter, fp1 must be greater than fs1.")

        elif filter_type == "passband" and not (fs1 < fp1 < fp2 < fs2):
            raise ValueError(
                f"For passband filter, expected fs1 < fp1 < fp2 < fs2, got {fs1}, {fp1}, {fp2}, {fs2}."
            )

        elif filter_type == "stopband" and not (fp1 < fs1 < fs2 < fp2):
            raise ValueError(
                f"For stopband filter, expected fp1 < fs1 < fs2 < fp2, got {fp1}, {fs1}, {fs2}, {fp2}."
            )

        elif filter_type not in ["lowpass", "highpass", "passband", "stopband"]:
            raise ValueError(f"Unsupported filter type: {filter_type}")

    def _validate_frequency_values(self):
        """
        Ensures frequency values are valid.
        """
        fp1, fp2, fs1, fs2, f = self._extract_frequencies()
        filter_type = self.filter_conf["filter_type"]

        # Ensure all frequencies are positive
        self._validate_frequencies_grater_than(
            ["passband_freq_hz", "stopband_freq_hz", "sampling_freq_hz"], 0
        )

        if filter_type in ["passband", "stopband"]:
            self._validate_frequencies_grater_than(
                ["passband_freq2_hz", "stopband_freq2_hz"], 0
            )

        # Ensure frequencies are less than Nyquist frequency (f/2)
        self._validate_frequencies_less_than(
            ["passband_freq_hz", "stopband_freq_hz"],
            self.filter_conf["sampling_freq_hz"] / 2,
        )

        if filter_type in ["passband", "stopband"]:
            self._validate_frequencies_less_than(
                ["passband_freq2_hz", "stopband_freq2_hz"],
                self.filter_conf["sampling_freq_hz"] / 2,
            )
