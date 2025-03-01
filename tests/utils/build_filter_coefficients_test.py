"""
This file contains tests for the truncate function in the utils module.
"""

from easy_fir_filter.utils import build_filter_coefficients


class TestBuildFilterCoefficientsUtilFunction:
    """
    Tests for the build_filter_coefficients function.
    """

    def test_build_filter_coefficients_symmetric(self):
        """
        Test build_filter_coefficients function with symmetric coefficients.
        """
        assert build_filter_coefficients([0.2, 0.5, 0.2]) == [0.2, 0.5, 0.2, 0.5, 0.2]

    def test_build_filter_coefficients_negative_zero(self):
        """
        Test build_filter_coefficients function with negative zero.
        """
        assert build_filter_coefficients([0.2, -0.0, 0.2]) == [0.2, 0, 0.2, 0, 0.2]

    def test_build_filter_coefficients_single_element(self):
        """
        Test build_filter_coefficients function with a single element.
        """
        assert build_filter_coefficients([0.5]) == [0.5]

    def test_build_filter_coefficients_empty(self):
        """
        Test build_filter_coefficients function with an empty list.
        """
        assert build_filter_coefficients([]) == []

    def test_build_filter_coefficients_large_values(self):
        """
        Test build_filter_coefficients function with large values.
        """
        assert build_filter_coefficients([1e10, 1e-10, 1e10]) == [
            1e10,
            1e-10,
            1e10,
            1e-10,
            1e10,
        ]
