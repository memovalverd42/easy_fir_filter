"""
This module contains the FilterConfValuesValidator class, which is used to validate the values of the filter configuration.

The FilterConfValuesValidator ensures that the filter configuration parameters, such as ripples, frequencies, and filter type,
meet the necessary criteria for a valid FIR filter design.
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
    This class is used to validate the values of the filter configuration.

    It checks for valid ranges, relationships between parameters, and consistency based on the filter type.

    Attributes:
        filter_conf (FilterConf): The filter configuration dictionary to validate.
    """

    def __init__(self, filter_conf: FilterConf):
        """
        Initializes the validator with the filter configuration and performs validation.

        Args:
            filter_conf (FilterConf): The filter configuration dictionary.
        """
        self.filter_conf = filter_conf
        self._validate_values()

    def _validate_values(self):
        """
        Runs all necessary validations on the filter configuration.

        This method orchestrates the validation process by calling individual validation methods.
        """
        self._validate_ripples()
        self._validate_frequency_values()
        self._validate_frequencies_by_filter_type()

    def _extract_frequencies(self):
        """
        Extracts the frequencies from the filter configuration.

        Returns:
            tuple: A tuple containing passband frequency 1, passband frequency 2, stopband frequency 1,
                   stopband frequency 2, and sampling frequency.
        """
        return (
            self.filter_conf.get("passband_freq_hz"),
            self.filter_conf.get("passband_freq2_hz"),
            self.filter_conf.get("stopband_freq_hz"),
            self.filter_conf.get("stopband_freq2_hz"),
            self.filter_conf["sampling_freq_hz"],
        )

    def _validate_frequencies_grater_than(
        self, keys: list[_KEYS_LITERAL], value: int | float
    ):
        """
        Ensures specified frequencies are greater than a given value.

        Args:
            keys (list[_KEYS_LITERAL]): A list of frequency keys to validate.
            value (int | float): The minimum allowed value for the frequencies.

        Raises:
            ValueError: If any specified frequency is not greater than the given value.
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

        Args:
            keys (list[_KEYS_LITERAL]): A list of frequency keys to validate.
            value (int | float): The maximum allowed value for the frequencies.

        Raises:
            ValueError: If any specified frequency is greater than the given value.
        """
        invalid_frequency = [
            key
            for key in keys
            if self.filter_conf[key] is not None and self.filter_conf[key] > value
        ]
        if invalid_frequency:
            raise ValueError(
                f'{", ".join(invalid_frequency)} must be less than or equal to {value}'
            )

    def _validate_ripples(self):
        """
        Validates the passband ripple and stopband attenuation values.

        Raises:
            ValueError: If ripples are not positive or if passband ripple is not less than stopband attenuation.
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
        Validates the frequency order based on the filter type.

        Raises:
            ValueError: If the frequency order is invalid for the specified filter type.
        """
        filter_type = self.filter_conf["filter_type"]
        fp1, fp2, fs1, fs2, _ = self._extract_frequencies()

        if filter_type == "lowpass" and fp1 >= fs1:
            raise ValueError("For lowpass filter, fp1 must be less than fs1.")

        elif filter_type == "highpass" and fp1 <= fs1:
            raise ValueError("For highpass filter, fp1 must be greater than fs1.")

        elif filter_type == "passband" and not (fs1 < fp1 < fp2 < fs2):
            raise ValueError(
                f"For bandpass filter, expected fs1 < fp1 < fp2 < fs2, got {fs1}, {fp1}, {fp2}, {fs2}."
            )

        elif filter_type == "bandstop" and not (fp1 < fs1 < fs2 < fp2):
            raise ValueError(
                f"For bandstop filter, expected fp1 < fs1 < fs2 < fp2, got {fp1}, {fs1}, {fs2}, {fp2}."
            )

        elif filter_type not in ["lowpass", "highpass", "bandpass", "bandstop"]:
            raise ValueError(f"Unsupported filter type: {filter_type}")

    def _validate_frequency_values(self):
        """
        Ensures frequency values are valid and within acceptable ranges.

        Raises:
            ValueError: If any frequency value is invalid or out of range.
        """
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

        if filter_type in ["bandpass", "bandstop"]:
            self._validate_frequencies_less_than(
                ["passband_freq2_hz", "stopband_freq2_hz"],
                self.filter_conf["sampling_freq_hz"] / 2,
            )
