"""
This file contains the implementation of the easy_fir_filter class.
"""
from easy_fir_filter.types import FilterConf
from easy_fir_filter.validators.filter_conf_validator import FilterConfValidator


class EasyFirFilter(FilterConfValidator):
    """
    Easy Filter Class
    """

    def __init__(self, filter_conf: FilterConf):
        """
        Constructor
        """
        self.filter_conf = filter_conf
        FilterConfValidator.__init__(self, filter_conf)
