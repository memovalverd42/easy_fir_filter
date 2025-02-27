"""
This file contains the tests for the Hamming window implementation.
"""

import pytest

from easy_fir_filter import FilterConf
from easy_fir_filter.windows.hamming_window import HammingWindow
from tests.fixtures.filter_configurations import filter_order_results

hamming_filter_configurations: list[FilterConf] = [
    {
        "filter_type": "highpass",
        "window_type": "hamming",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 34,
    },
    {
        "filter_type": "lowpass",
        "window_type": "hamming",
        "sampling_freq_hz": 2500,
        "passband_freq_hz": 500,
        "stopband_freq_hz": 750,
        "passband_ripple_db": 0.1,
        "stopband_attenuation_db": 44,
    },
    {
        "filter_type": "highpass",
        "window_type": "hamming",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_ripple_db": 0.3,
        "stopband_attenuation_db": 35,
    },
    {
        "filter_type": "bandstop",
        "window_type": "hamming",
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
        "window_type": "hamming",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_freq2_hz": 24,
        "stopband_freq2_hz": 32,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 34,
    },
]

correct_hamming_results = [
    [
        1.0,
        0.9774859,
        0.9121478,
        0.8103812,
        0.6821478,
        0.54,
        0.3978521,
        0.2696187,
        0.1678521,
        0.102514,
        0.08,
    ],
    [
        1.0,
        0.9866332,
        0.9473097,
        0.8843149,
        0.8013097,
        0.7031182,
        0.5954468,
        0.4845531,
        0.3768817,
        0.2786902,
        0.195685,
        0.1326902,
        0.0933667,
        0.08,
    ],
    [
        1.0,
        0.9774859,
        0.9121478,
        0.8103812,
        0.6821478,
        0.54,
        0.3978521,
        0.2696187,
        0.1678521,
        0.102514,
        0.08,
    ],
    [
        1.0,
        0.9911612,
        0.9649845,
        0.922476,
        0.8652691,
        0.7955623,
        0.7160343,
        0.6297415,
        0.54,
        0.4502584,
        0.3639656,
        0.2844376,
        0.2147308,
        0.1575239,
        0.1150154,
        0.0888387,
        0.08,
    ],
    [
        1.0,
        0.9774859,
        0.9121478,
        0.8103812,
        0.6821478,
        0.54,
        0.3978521,
        0.2696187,
        0.1678521,
        0.102514,
        0.08,
    ],
]


class TestHammingWindow:
    """
    Test class for the Hamming window.
    """

    @pytest.fixture
    def window_builder(self) -> HammingWindow:
        """
        Fixture to create a HammingWindow instance.
        """
        return HammingWindow(round_to=7)

    @pytest.mark.parametrize("order", filter_order_results)
    def test_calculate_window_coefficients_returns_list(
        self, window_builder: HammingWindow, order: tuple[int, int]
    ):
        """
        Test that the calculate_window_coefficients method returns a list.
        """
        n, N = order
        result = window_builder.calculate_window_coefficients(n, N, AS=None)
        assert isinstance(result, list)

    @pytest.mark.parametrize("order", filter_order_results)
    def test_calculate_window_coefficients_returns_list_of_floats(
        self, window_builder: HammingWindow, order: tuple[int, int]
    ):
        """
        Test that the calculate_window_coefficients method returns a list of floats.
        """
        n, N = order
        result = window_builder.calculate_window_coefficients(n, N, AS=None)
        assert all(isinstance(x, float) for x in result)

    @pytest.mark.parametrize("order", filter_order_results)
    def test_calculate_window_coefficients_has_correct_length(
        self, window_builder: HammingWindow, order: tuple[int, int]
    ):
        """
        Test that the calculate_window_coefficients method returns a list of the correct length.
        """
        n, N = order
        result = window_builder.calculate_window_coefficients(n, N, AS=None)
        assert len(result) == n + 1

    def test_calculate_window_coefficients_raises_error_if_n_or_filter_length_is_none(
        self, window_builder: HammingWindow
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
        "order, expected_result", zip(filter_order_results, correct_hamming_results)
    )
    def test_calculate_window_coefficients_has_correct_values(
        self,
        window_builder: HammingWindow,
        order: tuple[int, int],
        expected_result: list[float],
    ):
        """
        Test that the calculate_window_coefficients method returns the correct values.
        """
        n, N = order
        result = window_builder.calculate_window_coefficients(n, N, AS=None)
        assert result == expected_result
