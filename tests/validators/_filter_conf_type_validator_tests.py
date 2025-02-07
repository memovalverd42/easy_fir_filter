"""
This file contains the tests for the FilterConfTypeValidator class.
"""

import pytest

from easy_fir_filter import FilterConf
from easy_fir_filter.exceptions import MissingKeysError, InvalidTypeError
from easy_fir_filter.validators._filter_conf_type_validator import (  # type: ignore
    _FilterConfTypeValidator,
    _REQUIRED_KEYS,
    _OPTIONAL_KEYS,
)

INVALID_KEYS_TYPES = [
    ("filter_type", 1),
    ("window_type", 1),
    ("sampling_freq_hz", "140000"),
    ("passband_freq_hz", "40000"),
    ("stopband_freq_hz", "50000"),
    ("passband_ripple_db", "1"),
    ("stopband_attenuation_db", "40"),
]

INVALID_OPTIONAL_KEYS_TYPES = [
    ("passband_freq2_hz", "20000"),
    ("stopband_freq2_hz", "60000"),
]


class TestFilterConfTypeValidator:
    """
    This class contains tests for the FilterConfTypeValidator class.
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

    @pytest.mark.parametrize(
        "missing_key",
        _REQUIRED_KEYS.keys(),
    )
    def test_validate_required_keys_raises_missing_keys_error(
        self, valid_filter_conf: FilterConf, missing_key: str
    ):
        """
        Tests that the _validate_required_keys method raises a MissingKeysError when a required key is missing.
        """
        valid_filter_conf.pop(missing_key)  # type: ignore

        with pytest.raises(
            MissingKeysError, match=f"Missing required keys: {missing_key}"
        ):
            _FilterConfTypeValidator(valid_filter_conf)

    def test_validate_required_keys_does_not_raise_missing_keys_error(
        self, valid_filter_conf: FilterConf
    ):
        """
        Tests that the _validate_required_keys method does not raise a MissingKeysError when all required keys are present.
        """
        _FilterConfTypeValidator(valid_filter_conf)

    @pytest.mark.parametrize(
        "key, invalid_value",
        INVALID_KEYS_TYPES,
    )
    def test_validate_values_types_raises_invalid_type_error(
        self, valid_filter_conf: FilterConf, key: str, invalid_value: int | str
    ):
        """
        Tests that the _validate_values_types method raises an InvalidTypeError when a value has an invalid type.
        """
        valid_filter_conf[key] = invalid_value  # type: ignore
        with pytest.raises(InvalidTypeError):
            _FilterConfTypeValidator(valid_filter_conf)

    def test_validate_values_types_does_not_raise_invalid_type_error(
        self, valid_filter_conf: FilterConf
    ):
        """
        Tests that the _validate_values_types method does not raise an InvalidTypeError when all values have valid types.
        """
        _FilterConfTypeValidator(valid_filter_conf)

    @pytest.mark.parametrize(
        "missing_key",
        _OPTIONAL_KEYS.keys(),
    )
    def test_validate_optional_keys_raises_missing_keys_error(
        self, valid_filter_conf_2: FilterConf, missing_key: str
    ):
        """
        Tests that the _validate_optional_keys method raises a MissingKeysError when a required key is missing.
        """
        valid_filter_conf_2.pop(missing_key)  # type: ignore
        with pytest.raises(
            MissingKeysError, match=f"Missing required keys: {missing_key}"
        ):
            _FilterConfTypeValidator(valid_filter_conf_2)

    def test_validate_optional_keys_does_not_raise_missing_keys_error(
        self, valid_filter_conf_2: FilterConf
    ):
        """
        Tests that the _validate_optional_keys method does not raise a MissingKeysError when all required keys are present.
        """
        _FilterConfTypeValidator(valid_filter_conf_2)

    @pytest.mark.parametrize(
        "key, invalid_value",
        INVALID_OPTIONAL_KEYS_TYPES,
    )
    def test_validate_optional_keys_raises_invalid_type_error(
        self, valid_filter_conf_2: FilterConf, key: str, invalid_value: str
    ):
        """
        Tests that the _validate_optional_keys method raises an InvalidTypeError when a value has an invalid type.
        """
        valid_filter_conf_2[key] = invalid_value  # type: ignore
        with pytest.raises(InvalidTypeError):
            _FilterConfTypeValidator(valid_filter_conf_2)

    def test_validate_optional_keys_does_not_raise_invalid_type_error(
        self, valid_filter_conf_2: FilterConf
    ):
        """
        Tests that the _validate_optional_keys method does not raise an InvalidTypeError when all values have valid types.
        """
        _FilterConfTypeValidator(valid_filter_conf_2)

    def test_validate_filter_type_raises_value_error(
        self, valid_filter_conf: FilterConf
    ):
        """
        Tests that the _validate_filter_type method raises a ValueError when the filter type is invalid.
        """
        valid_filter_conf["filter_type"] = "invalid"  # type: ignore
        with pytest.raises(ValueError):
            _FilterConfTypeValidator(valid_filter_conf)

    def test_validate_filter_type_does_not_raise_value_error(
        self, valid_filter_conf: FilterConf
    ):
        """
        Tests that the _validate_filter_type method does not raise a ValueError when the filter type is valid.
        """
        _FilterConfTypeValidator(valid_filter_conf)

    def test_validate_window_type_raises_value_error(
        self, valid_filter_conf: FilterConf
    ):
        """
        Tests that the _validate_window_type method raises a ValueError when the window type is invalid.
        """
        valid_filter_conf["window_type"] = "invalid"  # type: ignore
        with pytest.raises(ValueError):
            _FilterConfTypeValidator(valid_filter_conf)

    def test_validate_window_type_does_not_raise_value_error(
        self, valid_filter_conf: FilterConf
    ):
        """
        Tests that the _validate_window_type method does not raise a ValueError when the window type is valid.
        """
        _FilterConfTypeValidator(valid_filter_conf)
