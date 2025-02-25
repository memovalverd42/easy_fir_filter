"""
Tests for the calculate_delta method of the EasyFirFilter class.
"""

import pytest

from tests.easy_fir_filter.easy_fir_filter_tests import TestBaseEasyFirFilter
from tests.fixtures.filter_configurations import (
    list_filter_configurations,
    delta_results,
)


class TestCalculateDelta(TestBaseEasyFirFilter):
    """
    Tests for the calculate_delta method of the EasyFirFilter class.
    """

    @pytest.mark.parametrize(
        "filter_conf",
        list_filter_configurations,
    )
    def test_calculate_delta_returns_tuple_of_floats(self, easy_fir_filter_builder):
        """
        Tests that the calculate_delta method returns a float.
        """
        assert isinstance(easy_fir_filter_builder.calculate_delta(), float)

    @pytest.mark.parametrize(
        "filter_conf, expected_delta",
        list(zip(list_filter_configurations, delta_results)),
    )
    def test_calculate_delta_correct_value(
        self, easy_fir_filter_builder, expected_delta
    ):
        """
        Tests that the calculate_delta method returns the correct value.
        """
        assert (
            pytest.approx(easy_fir_filter_builder.calculate_delta(), 0.0001)
            == expected_delta
        )
