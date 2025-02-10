"""
This file contains the tests for the FilterConfValuesValidator class.
"""

import pytest

from easy_fir_filter import FilterConf
from easy_fir_filter.validators._filter_conf_values_validator import (
    _FilterConfValuesValidator,
)


class TestFilterConfValuesValidator:
    """
    This class contains tests for the FilterConfValuesValidator class.
    """

    @pytest.fixture
    def valid_filter_conf(self) -> FilterConf:
        """
        Returns a valid filter configuration.
        """
        return {
            "filter_type": "lowpass",
            "window_type": "blackman",
            "sampling_freq_hz": 140000,
            "passband_freq_hz": 40000,
            "stopband_freq_hz": 50000,
            "passband_ripple_db": 1,
            "stopband_attenuation_db": 40,
        }

    @pytest.fixture
    def valid_filter_conf_2(self) -> FilterConf:
        """
        Returns a valid filter configuration.
        """
        return {
            "filter_type": "passband",
            "window_type": "blackman",
            "sampling_freq_hz": 140000,
            "passband_freq_hz": 40000,
            "stopband_freq_hz": 50000,
            "passband_ripple_db": 1,
            "stopband_attenuation_db": 40,
            "passband_freq2_hz": 20000,
            "stopband_freq2_hz": 60000,
        }

    def test_validate_ripples_raises_value_error_for_non_positive_passband_ripple(
        self, valid_filter_conf
    ):
        """
        Tests that the _validate_ripples method raises a ValueError when passband ripple is not positive.
        """
        valid_filter_conf["passband_ripple_db"] = 0  # type: ignore
        with pytest.raises(ValueError, match="Passband ripple must be positive"):
            _FilterConfValuesValidator(valid_filter_conf)

    def test_validate_ripples_raises_value_error_for_non_positive_stopband_attenuation(
        self, valid_filter_conf
    ):
        """
        Tests that the _validate_ripples method raises a ValueError when stopband attenuation is not positive.
        """
        valid_filter_conf["stopband_attenuation_db"] = 0  # type: ignore
        with pytest.raises(ValueError, match="Stopband attenuation must be positive"):
            _FilterConfValuesValidator(valid_filter_conf)

    def test_validate_ripples_raises_value_error_for_passband_ripple_greater_than_or_equal_to_stopband_attenuation(
        self, valid_filter_conf
    ):
        """
        Tests that the _validate_ripples method raises a ValueError when passband ripple is greater than or equal to stopband attenuation.
        """
        valid_filter_conf["passband_ripple_db"] = 50  # type: ignore
        valid_filter_conf["stopband_attenuation_db"] = 40  # type: ignore
        with pytest.raises(
            ValueError, match="Passband ripple must be less than stopband attenuation"
        ):
            _FilterConfValuesValidator(valid_filter_conf)

    def test_validate_ripples_does_not_raise_error_for_valid_ripples(
        self, valid_filter_conf
    ):
        """
        Tests that the _validate_ripples method does not raise an error when ripples are valid.
        """
        _FilterConfValuesValidator(valid_filter_conf)

    def test_validate_frequencies_by_filter_type_raises_value_error_for_invalid_lowpass(
        self, valid_filter_conf
    ):
        """
        Tests that the _validate_frequencies_by_filter_type method raises a ValueError
        for invalid lowpass filter configuration.
        """
        valid_filter_conf["filter_type"] = "lowpass"  # type: ignore
        valid_filter_conf["passband_freq_hz"] = 50000
        valid_filter_conf["stopband_freq_hz"] = 40000
        with pytest.raises(
            ValueError, match="For lowpass filter, fp1 must be less than fs1."
        ):
            _FilterConfValuesValidator(valid_filter_conf)

    def test_validate_frequencies_by_filter_type_raises_value_error_for_invalid_highpass(
        self, valid_filter_conf
    ):
        """
        Tests that the _validate_frequencies_by_filter_type method raises
        a ValueError for invalid highpass filter configuration.
        """
        valid_filter_conf["filter_type"] = "highpass"  # type: ignore
        valid_filter_conf["passband_freq_hz"] = 40000
        valid_filter_conf["stopband_freq_hz"] = 50000
        with pytest.raises(
            ValueError, match="For highpass filter, fp1 must be greater than fs1."
        ):
            _FilterConfValuesValidator(valid_filter_conf)

    def test_validate_frequencies_by_filter_type_raises_value_error_for_invalid_passband(
        self, valid_filter_conf_2
    ):
        """
        Tests that the _validate_frequencies_by_filter_type method
        raises a ValueError for invalid passband filter configuration.
        """
        valid_filter_conf_2["filter_type"] = "passband"  # type: ignore
        valid_filter_conf_2["passband_freq_hz"] = 60000
        valid_filter_conf_2["passband_freq2_hz"] = 50000
        with pytest.raises(
            ValueError, match="For passband filter, expected fs1 < fp1 < fp2 < fs2"
        ):
            _FilterConfValuesValidator(valid_filter_conf_2)

    def test_validate_frequencies_by_filter_type_raises_value_error_for_invalid_stopband(
        self, valid_filter_conf_2
    ):
        """
        Tests that the _validate_frequencies_by_filter_type method raises a ValueError for invalid stopband filter configuration.
        """
        valid_filter_conf_2["filter_type"] = "stopband"  # type: ignore
        valid_filter_conf_2["passband_freq_hz"] = 50000
        valid_filter_conf_2["stopband_freq_hz"] = 40000
        valid_filter_conf_2["stopband_freq2_hz"] = 60000
        valid_filter_conf_2["passband_freq2_hz"] = 70000
        with pytest.raises(
            ValueError, match="For stopband filter, expected fp1 < fs1 < fs2 < fp2"
        ):
            _FilterConfValuesValidator(valid_filter_conf_2)

    def test_validate_frequencies_by_filter_type_does_not_raise_error_for_valid_configuration(
        self, valid_filter_conf, valid_filter_conf_2
    ):
        """
        Tests that the _validate_frequencies_by_filter_type method does not raise an error for valid filter configurations.
        """
        _FilterConfValuesValidator(valid_filter_conf)
        _FilterConfValuesValidator(valid_filter_conf_2)

    def test_validate_frequency_values_raises_value_error_for_non_positive_frequencies(
        self, valid_filter_conf
    ):
        """
        Tests that the _validate_frequency_values method raises a ValueError when frequencies are not positive.
        """
        valid_filter_conf["passband_freq_hz"] = 0  # type: ignore
        with pytest.raises(ValueError, match="passband_freq_hz must be greater than 0"):
            _FilterConfValuesValidator(valid_filter_conf)

    def test_validate_frequency_values_raises_value_error_for_frequencies_greater_than_nyquist(
        self, valid_filter_conf
    ):
        """
        Tests that the _validate_frequency_values method raises a ValueError when frequencies are greater than the Nyquist frequency.
        """
        valid_filter_conf["passband_freq_hz"] = 80000  # type: ignore
        with pytest.raises(
            ValueError, match="passband_freq_hz must be less than or equal to 70000.0"
        ):
            _FilterConfValuesValidator(valid_filter_conf)

    def test_validate_frequency_values_does_not_raise_error_for_valid_frequencies(
        self, valid_filter_conf, valid_filter_conf_2
    ):
        """
        Tests that the _validate_frequency_values method does not raise an error for valid frequencies.
        """
        _FilterConfValuesValidator(valid_filter_conf)
        _FilterConfValuesValidator(valid_filter_conf_2)
