"""
This module contains the FilterConfValidator class, which validates the filter configuration.

The FilterConfValidator class combines type and value validations to ensure the filter configuration
is both structurally correct and contains valid parameter values for FIR filter design.
"""

from easy_fir_filter.types.fir_filter_conf import FilterConf
from easy_fir_filter.validators._filter_conf_type_validator import \
    _FilterConfTypeValidator
from easy_fir_filter.validators._filter_conf_values_validator import \
    _FilterConfValuesValidator


class FilterConfValidator(_FilterConfTypeValidator, _FilterConfValuesValidator):
    """
    This class validates the filter configuration by combining type and value validations.

    It inherits from _FilterConfTypeValidator and _FilterConfValuesValidator to ensure that
    the filter configuration dictionary has the correct structure and valid parameter values.

    Attributes:
        filter_conf (FilterConf): The filter configuration dictionary to validate.
    """

    def __init__(self, filter_conf: FilterConf):
        """
        Initializes the FilterConfValidator with the filter configuration and performs both type and value validations.

        Args:
            filter_conf (FilterConf): The filter configuration dictionary.
        """
        self.filter_conf = filter_conf
        _FilterConfTypeValidator.__init__(self, filter_conf)
        _FilterConfValuesValidator.__init__(self, filter_conf)
        # TODO: Add validations to avoid high computational cost
        # This TODO comment indicates a planned enhancement to include checks for computationally expensive configurations.
        # For example, extremely narrow transition bands or very high filter orders.
