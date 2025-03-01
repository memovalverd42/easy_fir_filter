"""
This file contains the tests for the Blackman window implementation.
"""

import pytest

from easy_fir_filter import FilterConf
from easy_fir_filter.windows.blackman_window import BlackmanWindow
from tests.fixtures.filter_configurations import filter_order_results

blackman_filter_configurations: list[FilterConf] = [
    {
        "filter_type": "highpass",
        "window_type": "blackman",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 34,
    },
    {
        "filter_type": "lowpass",
        "window_type": "blackman",
        "sampling_freq_hz": 2500,
        "passband_freq_hz": 500,
        "stopband_freq_hz": 750,
        "passband_ripple_db": 0.1,
        "stopband_attenuation_db": 44,
    },
    {
        "filter_type": "highpass",
        "window_type": "blackman",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_ripple_db": 0.3,
        "stopband_attenuation_db": 35,
    },
    {
        "filter_type": "bandstop",
        "window_type": "blackman",
        "sampling_freq_hz": 13000,
        "passband_freq_hz": 2000,
        "stopband_freq_hz": 3000,
        "passband_freq2_hz": 5000,
        "stopband_freq2_hz": 4000,
        "passband_ripple_db": 0.2,
        "stopband_attenuation_db": 43,
    },
    {
        "filter_type": "bandpass",
        "window_type": "blackman",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_freq2_hz": 24,
        "stopband_freq2_hz": 32,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 34,
    },
]

correct_blackman_results = [
    [
        0.9999999,
        0.9602496,
        0.8492298,
        0.6891712,
        0.5097871,
        0.34,
        0.2007701,
        0.101386,
        0.0402128,
        0.0091931,
        0.0,
    ],
    [
        0.9999999,
        0.9763073,
        0.9081731,
        0.8038983,
        0.6756639,
        0.5374215,
        0.4025929,
        0.2820563,
        0.1828166,
        0.1075992,
        0.0553875,
        0.0227171,
        0.0053655,
        0.0,
    ],
    [
        0.9999999,
        0.9602496,
        0.8492298,
        0.6891712,
        0.5097871,
        0.34,
        0.2007701,
        0.101386,
        0.0402128,
        0.0091931,
        0.0,
    ],
    [
        0.9999999,
        0.984303,
        0.9385083,
        0.8663494,
        0.7735533,
        0.6671704,
        0.5547731,
        0.4436347,
        0.34,
        0.2485444,
        0.1720897,
        0.1116002,
        0.0664466,
        0.0348798,
        0.0146287,
        0.0035177,
        0.0,
    ],
    [
        0.9999999,
        0.9602496,
        0.8492298,
        0.6891712,
        0.5097871,
        0.34,
        0.2007701,
        0.101386,
        0.0402128,
        0.0091931,
        0.0,
    ],
]


class TestBlackmanWindow:
    """
    Test suite for the Blackman window implementation.
    """

    @pytest.fixture
    def window_builder(self) -> BlackmanWindow:
        """
        Fixture for the Blackman window builder.

        Returns:
            BlackmanWindow: A Blackman window instance.
        """
        return BlackmanWindow(round_to=7)

    @pytest.mark.parametrize("order", filter_order_results)
    def test_calculate_window_coefficients_returns_list(
        self, window_builder: BlackmanWindow, order: tuple[int, int]
    ):
        """
        Test that the calculate_window_coefficients method returns a list.
        """
        n, N = order
        result = window_builder.calculate_window_coefficients(n, N, AS=None)
        assert isinstance(result, list)

    @pytest.mark.parametrize("order", filter_order_results)
    def test_calculate_window_coefficients_returns_list_of_floats(
        self, window_builder: BlackmanWindow, order: tuple[int, int]
    ):
        """
        Test that the calculate_window_coefficients method returns a list of floats.
        """
        n, N = order
        result = window_builder.calculate_window_coefficients(n, N, AS=None)
        assert all(isinstance(x, float) for x in result)

    @pytest.mark.parametrize("order", filter_order_results)
    def test_calculate_window_coefficients_has_correct_length(
        self, window_builder: BlackmanWindow, order: tuple[int, int]
    ):
        """
        Test that the calculate_window_coefficients method returns a list of the correct length.
        """
        n, N = order
        result = window_builder.calculate_window_coefficients(n, N, AS=None)
        assert len(result) == n + 1

    def test_calculate_window_coefficients_raises_error_if_n_or_filter_length_is_none(
        self, window_builder: BlackmanWindow
    ):
        """
        Test that the calculate_window_coefficients method raises an error if n or filter_length is None.
        """
        with pytest.raises(ValueError):
            window_builder.calculate_window_coefficients(
                n=None, filter_length=10, AS=None  # type: ignore
            )
        with pytest.raises(ValueError):
            window_builder.calculate_window_coefficients(
                n=10, filter_length=None, AS=None  # type: ignore
            )

    @pytest.mark.parametrize(
        "order, expected_result", zip(filter_order_results, correct_blackman_results)
    )
    def test_calculate_window_coefficients_has_correct_values(
        self,
        window_builder: BlackmanWindow,
        order: tuple[int, int],
        expected_result: list[float],
    ):
        """
        Test that the calculate_window_coefficients method returns the correct values.
        """
        n, N = order
        result = window_builder.calculate_window_coefficients(n, N, AS=None)
        assert result == expected_result
