"""
This module contains tests for the calculate_ripples method.
"""

import pytest

from tests.easy_fir_filter.easy_fir_filter_tests import TestBaseEasyFirFilter
from tests.fixtures.filter_configurations import (
    list_filter_configurations,
    ripples_results,
)


class TestCalculateRipples(TestBaseEasyFirFilter):
    """
    Tests for the calculate_ripples method of the EasyFirFilter class.
    """

    @pytest.mark.parametrize(
        "filter_conf",
        list_filter_configurations,
    )
    def test_calculate_ripples_returns_float(self, easy_fir_filter_builder):
        """
        Tests that the calculate_ripples method returns a float.
        """
        easy_fir_filter_builder.calculate_delta()

        As, Ap = easy_fir_filter_builder.calculate_ripples()

        assert isinstance(As, float)
        assert isinstance(Ap, float)

    @pytest.mark.parametrize(
        "filter_conf, expected_ripples",
        list(zip(list_filter_configurations, ripples_results)),
    )
    def test_calculate_ripples_correct_value(
        self, easy_fir_filter_builder, expected_ripples
    ):
        """
        Tests that the calculate_ripples method returns the correct value.
        """
        easy_fir_filter_builder.calculate_delta()

        As, Ap = easy_fir_filter_builder.calculate_ripples()
        expected_As, expected_Ap = expected_ripples
        assert pytest.approx(As, 0.0001) == expected_As
        assert pytest.approx(Ap, 0.0001) == expected_Ap
