"""
This file contains the tests for the easy_fir_filter class.
"""

import pytest

from easy_fir_filter import FilterConf
from easy_fir_filter.easy_fir_filter import EasyFirFilter


class TestBaseEasyFirFilter:

    @pytest.fixture
    def easy_fir_filter_builder(
        self, filter_conf: FilterConf, round_to: int = 7
    ) -> EasyFirFilter:
        """
        Returns an EasyFirFilter object.
        """
        return EasyFirFilter(filter_conf, round_to)
