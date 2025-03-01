"""
This file  contains tests for the truncate function in the utils module.
"""

import pytest

from easy_fir_filter.utils import truncate


class TestTruncateUtilFunction:
    """
    Tests for the truncate function.
    """

    def test_truncate_positive_number(self):
        """
        Test truncate function with positive numbers.
        """
        assert truncate(123.456789, 2) == 123.45
        assert truncate(123.456789, 0) == 123.0
        assert truncate(123.456789, 4) == 123.4567

    def test_truncate_negative_number(self):
        """
        Test truncate function with negative numbers.
        """
        assert truncate(-123.456789, 2) == -123.45
        assert truncate(-123.456789, 0) == -123.0
        assert truncate(-123.456789, 4) == -123.4567

    def test_truncate_zero(self):
        """
        Test truncate function with zero.
        """
        assert truncate(0.0, 2) == 0.0
        assert truncate(0.0, 0) == 0.0

    def test_truncate_large_decimals(self):
        """
        Test truncate function with large number of decimals.
        """
        assert truncate(1.999999999, 8) == 1.99999999

    def test_truncate_no_decimals(self):
        """
        Test truncate function with no decimals.
        """
        assert truncate(123.456789, 0) == 123.0

    def test_truncate_invalid_decimals(self):
        """
        Test truncate function with invalid number of decimals.
        """
        with pytest.raises(ValueError):
            truncate(123.456789, -1)
