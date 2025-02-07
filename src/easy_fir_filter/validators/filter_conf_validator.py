"""
This file contains the class that validates the filter configuration.
"""

from easy_fir_filter.types.fir_filter_conf import FilterConf
from easy_fir_filter.validators._filter_conf_type_validator import (
    _FilterConfTypeValidator,
)
from easy_fir_filter.validators._filter_conf_values_validator import (
    _FilterConfValuesValidator,
)


class FilterConfValidator(_FilterConfTypeValidator, _FilterConfValuesValidator):
    """
    This class validates the filter configuration.
    """

    def __init__(self, filter_conf: FilterConf):
        """
        Constructor
        """
        self.filter_conf = filter_conf
        _FilterConfTypeValidator.__init__(self, filter_conf)
        _FilterConfValuesValidator.__init__(self, filter_conf)
        # TODO: Add validations to avoid high computational cost
