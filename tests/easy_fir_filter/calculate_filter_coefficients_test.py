"""
This file contains tests for the calculate_filter_coefficients function in the easy_fir_filter module.
"""

import pytest

from tests.easy_fir_filter.easy_fir_filter_test import TestBaseEasyFirFilter
from tests.fixtures.filter_configurations import (
    list_filter_configurations,
    filter_order_results,
)


correct_filter_values = [
    [
        0.7,
        -0.2517203,
        -0.1380675,
        -0.0265705,
        0.031907,
        0.0343774,
        0.0124061,
        -0.0037886,
        -0.0063517,
        -0.0029332,
        0.0,
    ],
    [
        0.5,
        0.314055,
        0.0,
        -0.0938286,
        0.0,
        0.0447618,
        0.0,
        -0.0220339,
        0.0,
        0.0098566,
        0.0,
        -0.0038396,
        0.0,
        0.0019588,
    ],
    [
        0.7,
        -0.2546461,
        -0.1446905,
        -0.0295965,
        0.0388964,
        0.047479,
        0.0202416,
        -0.0076683,
        -0.0166462,
        -0.009611,
        0.0,
    ],
    [
        0.6923076,
        0.0354389,
        0.2480602,
        -0.0705916,
        -0.1190898,
        0.0409022,
        0.0150793,
        0.011846,
        0.0196589,
        -0.0340367,
        -0.0113204,
        0.0198606,
        0.0010574,
        0.0,
        -0.0005625,
        -0.0054917,
        0.0015405,
    ],
    [
        0.3999999,
        0.0,
        -0.2570878,
        0.0,
        0.04769,
        0.0,
        0.0125212,
        0.0,
        -0.0030434,
        0.0,
        0.0,
    ],
]


class TestCalculateFilterCoefficients(TestBaseEasyFirFilter):
    """
    Tests for the calculate_filter_coefficients function.
    """

    @pytest.fixture
    def precomputed_filter(self, easy_fir_filter_builder):
        """
        Returns an instance of EasyFirFilter with the
        all the methods precomputed.
        """
        # Delta
        easy_fir_filter_builder.calculate_delta()
        # Ripples A's and A'p
        easy_fir_filter_builder.calculate_ripples()
        # D parameter
        easy_fir_filter_builder.calculate_d_parameter()
        # Filter order
        n, N = easy_fir_filter_builder.filter.calculate_filter_order(easy_fir_filter_builder.D)  # type: ignore
        # Impulse response coefficients
        easy_fir_filter_builder.filter.calculate_impulse_response_coefficients()
        # Window coefficients
        if easy_fir_filter_builder.filter_conf["window_type"] == "kaiser":
            easy_fir_filter_builder.window.calculate_window_coefficients(n, N, easy_fir_filter_builder.AS)  # type: ignore
        else:
            easy_fir_filter_builder.window.calculate_window_coefficients(n, N)

        return easy_fir_filter_builder

    @pytest.mark.parametrize("filter_conf", list_filter_configurations)
    def test_calculate_filter_coefficients_returns_list_of_floats(
        self, precomputed_filter
    ):
        """
        Tests that the calculate_filter_coefficients function returns a list of floats.
        """
        assert isinstance(precomputed_filter._calculate_filter_coefficients(), list)

    @pytest.mark.parametrize(
        "filter_conf, order",
        list(zip(list_filter_configurations, filter_order_results)),
    )
    def test_calculate_filter_coefficients_returns_correct_length(
        self, precomputed_filter, order: tuple[int, int]
    ):
        """
        Tests that the calculate_filter_coefficients function returns a list of the correct length.
        """
        n, N = order
        assert len(precomputed_filter._calculate_filter_coefficients()) == n + 1

    @pytest.mark.parametrize(
        "filter_conf, correct_values",
        list(zip(list_filter_configurations, correct_filter_values)),
    )
    def test_calculate_filter_coefficients_returns_correct_values(
        self, precomputed_filter, correct_values: list[float]
    ):
        """
        Tests that the calculate_filter_coefficients function returns the correct values.
        """
        assert precomputed_filter._calculate_filter_coefficients() == correct_values
