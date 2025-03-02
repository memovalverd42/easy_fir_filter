"""
This file contains the implementation of the class that validates the filter configuration types.
"""

from typing import Dict, Literal

from easy_fir_filter.exceptions import InvalidTypeError, MissingKeysError
from easy_fir_filter.types.fir_filter_conf import FilterConf

_filter_keys = Literal[
    "filter_type",
    "window_type",
    "passband_ripple_db",
    "stopband_attenuation_db",
    "passband_freq_hz",
    "stopband_freq_hz",
    "sampling_freq_hz",
]

# Define required keys and their expected types
_REQUIRED_KEYS: Dict[_filter_keys, tuple[type]] = {
    "filter_type": (str,),
    "window_type": (str,),
    "passband_ripple_db": (float, int),
    "stopband_attenuation_db": (float, int),
    "passband_freq_hz": (float, int),
    "stopband_freq_hz": (float, int),
    "sampling_freq_hz": (float, int),
}  # type: ignore

_optional_keys = Literal["stopband_freq2_hz", "passband_freq2_hz"]

# Define optional keys and their expected types
_OPTIONAL_KEYS: Dict[_optional_keys, tuple[type, ...]] = {
    "stopband_freq2_hz": (float, int),
    "passband_freq2_hz": (float, int),
}

# Define valid values for filter_type
_FILTER_TYPE_VALUES: list[str] = ["bandstop", "lowpass", "highpass", "bandpass"]
# Define valid values for window_type
_WINDOW_TYPE_VALUES: list[str] = ["hamming", "blackman", "kaiser"]


class _FilterConfTypeValidator:
    """
    This class validates the types of the filter configuration.

    It ensures that the filter configuration dictionary contains all required keys
    with the correct data types and that the values for filter type and window type
    are valid.
    """

    def __init__(self, filter_conf: FilterConf):
        """
        Constructor

        Args:
            filter_conf (FilterConf): The filter configuration dictionary to validate.
        """
        self.filter_conf = filter_conf
        self._validate_types()

    def _validate_types(self):
        """
        Validates the types of the filter configuration.

        This method performs a series of validations to ensure that the filter
        configuration is valid. It checks for empty configurations, dictionary
        type, required and optional keys, value types, and valid filter and window types.
        """
        if not self.filter_conf:
            raise ValueError("Filter configuration is empty.")

        if not isinstance(self.filter_conf, dict):
            raise ValueError("Filter configuration must be a dictionary.")

        self._validate_required_keys()
        self._validate_values_types()
        self._validate_optional_keys()
        self._validate_filter_type()
        self._validate_window_type()

    def _validate_required_keys(self):
        """
        Validates the required keys of the filter configuration.

        This method checks if all required keys are present in the filter
        configuration dictionary.
        """
        conf_keys = set(self.filter_conf.keys())
        missing_keys = set(str(k) for k in _REQUIRED_KEYS.keys()) - conf_keys
        if missing_keys:
            raise MissingKeysError(list(missing_keys))

    def _validate_values_types(self):
        """
        Validates the values types of the filter configuration.

        This method checks if the values associated with the required keys
        have the correct data types.
        """
        for key in _REQUIRED_KEYS.keys():
            if not isinstance(self.filter_conf[key], _REQUIRED_KEYS[key]):
                raise InvalidTypeError(
                    key, _REQUIRED_KEYS[key][0], type(self.filter_conf[key])
                )

    def _validate_optional_keys(self):
        """
        Validates the optional keys of the filter configuration.

        This method checks if the optional keys are present when required
        (for bandstop and bandpass filters) and if their values have the
        correct data types.
        """
        types_required_optional = ["bandstop", "bandpass"]
        if self.filter_conf["filter_type"] in types_required_optional:
            conf_keys = set(self.filter_conf.keys())
            missing_keys = set(str(k) for k in _OPTIONAL_KEYS.keys()) - conf_keys
            if missing_keys:
                raise MissingKeysError(list(missing_keys))

        for key in _OPTIONAL_KEYS.keys():
            if key in self.filter_conf:
                value = self.filter_conf.get(key, None)  # type: ignore
                if value is not None and not isinstance(value, _OPTIONAL_KEYS[key]):
                    raise InvalidTypeError(
                        key, _OPTIONAL_KEYS[key][0], type(self.filter_conf[key])
                    )

    def _validate_filter_type(self):
        """
        Validates the filter type of the filter configuration.

        This method checks if the filter type is one of the valid values.
        """
        filter_type = self.filter_conf["filter_type"]
        if filter_type not in _FILTER_TYPE_VALUES:
            raise ValueError(f"Invalid filter type: {filter_type}")

    def _validate_window_type(self):
        """
        Validates the window type of the filter configuration.

        This method checks if the window type is one of the valid values.
        """
        window_type = self.filter_conf["window_type"]
        if window_type not in _WINDOW_TYPE_VALUES:
            raise ValueError(f"Invalid window type: {window_type}")
