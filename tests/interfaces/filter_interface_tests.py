from unittest.mock import Mock

import pytest
from easy_fir_filter.interfaces.filter_interface import IFilter
from tests.fixtures.filter_configurations import (
    filter_length_results,
    d_results,
    filter_order_results,
)


class ConcreteFilter(IFilter):
    def _calculate_filter_length(self, d: float) -> int:
        return int(d * 10)  # Implementación de ejemplo

    def calculate_impulse_response_coefficients(self) -> list[float]:
        return [0.1, 0.2, 0.3]  # Implementación de ejemplo


class TestConcreteFilter:
    """
    Tests for the ConcreteFilter class, which implements the IFilter interface.
    """

    @pytest.fixture
    def filter_instance(self):
        """
        Fixture that returns an instance of the ConcreteFilter class.
        """
        return ConcreteFilter()

    def test_calculate_filter_order_must_return_tuple(self, filter_instance: IFilter):
        """
        Test that the calculate_filter_order method returns a tuple.
        """
        result = filter_instance.calculate_filter_order(0.1)
        assert isinstance(result, tuple)

    def test_calculate_filter_order_must_return_tuple_of_integers(
        self, filter_instance: IFilter
    ):
        """
        Test that the calculate_filter_order method returns a tuple of integers.
        """
        result = filter_instance.calculate_filter_order(0.1)
        assert all(isinstance(i, int) for i in result)

    @pytest.mark.parametrize(
        "expected_length, d, expected_order",
        list(zip(filter_length_results, d_results, filter_order_results)),
    )
    def test_calculate_filter_order_must_return_correct_values(
        self,
        filter_instance: IFilter,
        expected_length: int,
        d: float,
        expected_order: tuple[int, int],
    ):
        """
        Test that the calculate_filter_order method returns the correct values.
        """
        filter_mock = Mock(spec=IFilter)

        filter_mock._calculate_filter_length.return_value = expected_length
        filter_instance._calculate_filter_length = filter_mock._calculate_filter_length

        n, N = filter_instance.calculate_filter_order(d)

        # Return correct values
        assert n == expected_order[0]
        assert N == expected_order[1]

        # Ensure that the mock method was called
        filter_mock._calculate_filter_length.assert_called_once_with(d)

        # Ensure that N is odd
        assert N % 2 == 1

        # Ensure that the n is symmetric with N
        assert n == (N - 1) / 2

    def test_calculate_filter_order_raises_value_error(self, filter_instance: IFilter):
        """
        Test that the calculate_filter_order method raises a ValueError when d is None.
        """
        with pytest.raises(ValueError):
            filter_instance.calculate_filter_order(None)
