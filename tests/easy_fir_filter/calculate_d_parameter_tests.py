"""
This file contains the tests for the calculate_d_parameter method.
"""

import pytest

from tests.easy_fir_filter.easy_fir_filter_tests import TestBaseEasyFirFilter
from tests.fixtures.filter_configurations import list_filter_configurations, d_results


class TestCalculateDParameter(TestBaseEasyFirFilter):
    """
    Tests for the calculate_d_parameter method of the EasyFirFilter class.
    """

    @pytest.fixture
    def precomputed_filter(self, easy_fir_filter_builder):
        """
        Returns an instance of EasyFirFilter with the
        delta and ripples precomputed.
        """
        easy_fir_filter_builder.calculate_delta()
        easy_fir_filter_builder.calculate_ripples()

        return easy_fir_filter_builder

    @pytest.mark.parametrize(
        "filter_conf",
        list_filter_configurations,
    )
    def test_calculate_d_parameter_returns_float(self, precomputed_filter):
        """
        Tests that the calculate_d_parameter method returns a float.
        """
        D = precomputed_filter.calculate_d_parameter()

        assert isinstance(D, float)

    @pytest.mark.parametrize(
        "filter_conf, expected_d",
        list(zip(list_filter_configurations, d_results)),
    )
    def test_calculate_d_parameter_correct_value(self, precomputed_filter, expected_d):
        """
        Tests that the calculate_d_parameter method returns the correct value.
        """
        D = precomputed_filter.calculate_d_parameter()
        assert pytest.approx(D, 0.0001) == expected_d
