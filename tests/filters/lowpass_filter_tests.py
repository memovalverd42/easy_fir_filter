"""
This file contains tests for the lowpass filter.
"""

import pytest

from easy_fir_filter import FilterConf
from easy_fir_filter.filters.lowpass_filter import LowpassFilter
from easy_fir_filter.interfaces.filter_interface import IFilter

lowpass_filter_configurations: list[FilterConf] = [
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
        "filter_type": "lowpass",
        "window_type": "kaiser",
        "sampling_freq_hz": 8000,
        "passband_freq_hz": 1000,
        "stopband_freq_hz": 1500,
        "passband_ripple_db": 0.2,
        "stopband_attenuation_db": 50,
    },
    {
        "filter_type": "lowpass",
        "window_type": "hamming",
        "sampling_freq_hz": 16000,
        "passband_freq_hz": 2000,
        "stopband_freq_hz": 3000,
        "passband_ripple_db": 0.3,
        "stopband_attenuation_db": 60,
    },
    {
        "filter_type": "lowpass",
        "window_type": "hamming",
        "sampling_freq_hz": 1000,
        "passband_freq_hz": 150,
        "stopband_freq_hz": 200,
        "passband_ripple_db": 0.15,
        "stopband_attenuation_db": 40,
    },
    {
        "filter_type": "lowpass",
        "window_type": "hamming",
        "sampling_freq_hz": 500,
        "passband_freq_hz": 50,
        "stopband_freq_hz": 75,
        "passband_ripple_db": 0.5,
        "stopband_attenuation_db": 35,
    },
]

lowpass_d_results = [
    2.5659562,
    2.9282878,
    3.6246518,
    2.3207072,
    1.8837079,
]

lowpass_N_results = [
    26,
    47,
    58,
    47,
    38,
]

lowpass_order_results = [
    (13, 27),
    (24, 49),
    (29, 59),
    (24, 49),
    (19, 39),
]

correct_impulse_response_coefficients = [
    [
        0.5,
        0.3183098,
        0.0,
        -0.1061032,
        0.0,
        0.0636619,
        0.0,
        -0.0454728,
        0.0,
        0.0353677,
        0.0,
        -0.0289372,
        0.0,
        0.0244853,
    ],
    [
        0.3125,
        0.2646649,
        0.1470399,
        0.0206997,
        -0.0562697,
        -0.0624387,
        -0.0203019,
        0.0252633,
        0.0397887,
        0.0196492,
        -0.0121811,
        -0.0283812,
        -0.0187565,
        0.0047768,
        0.0210057,
        0.0176443,
        0.0,
        -0.0155685,
        -0.0163377,
        -0.0032683,
        0.0112539,
        0.0148663,
        0.0055369,
        -0.0076888,
        -0.0132629,
    ],
    [
        0.3125,
        0.2646649,
        0.1470399,
        0.0206997,
        -0.0562697,
        -0.0624387,
        -0.0203019,
        0.0252633,
        0.0397887,
        0.0196492,
        -0.0121811,
        -0.0283812,
        -0.0187565,
        0.0047768,
        0.0210057,
        0.0176443,
        0.0,
        -0.0155685,
        -0.0163377,
        -0.0032683,
        0.0112539,
        0.0148663,
        0.0055369,
        -0.0076888,
        -0.0132629,
        -0.0070737,
        0.004685,
        0.0115627,
        0.0080385,
        -0.0021413,
    ],
    [
        0.35,
        0.2836161,
        0.128759,
        -0.0165982,
        -0.0756826,
        -0.0450158,
        0.0163938,
        0.0449129,
        0.0233872,
        -0.0160566,
        -0.0318309,
        -0.0131372,
        0.0155914,
        0.0241839,
        0.0070259,
        -0.0150052,
        -0.0189206,
        -0.002929,
        0.0143065,
        0.0149271,
        0.0,
        -0.0135055,
        -0.0117053,
        0.0021649,
        0.0126137,
    ],
    [
        0.25,
        0.225079,
        0.1591549,
        0.0750263,
        0.0,
        -0.0450158,
        -0.0530516,
        -0.0321541,
        0.0,
        0.0250087,
        0.0318309,
        0.0204617,
        0.0,
        -0.0173137,
        -0.0227364,
        -0.0150052,
        0.0,
        0.0132399,
        0.0176838,
        0.0118462,
    ],
]


class TestLowpassFilter:
    """
    Test class for the LowpassFilter class.
    """

    @pytest.fixture
    def filter_builder(self, filter_conf: FilterConf, round_to: int = 7) -> IFilter:
        """
        Returns an EasyFirFilter object.
        """
        return LowpassFilter(filter_conf, round_to)

    @pytest.mark.parametrize(
        "filter_conf, d",
        list(zip(lowpass_filter_configurations, lowpass_d_results)),
    )
    def test_calculate_filter_length_returns_int(
        self, filter_builder: IFilter, d: float
    ):
        """
        Test that the _calculate_filter_length method returns an integer.
        """
        assert isinstance(filter_builder._calculate_filter_length(d), int)

    @pytest.mark.parametrize(
        "filter_conf, d, N",
        list(zip(lowpass_filter_configurations, lowpass_d_results, lowpass_N_results)),
    )
    def test_calculate_filter_length_correct_value(
        self, filter_builder: IFilter, d: float, N: int
    ):
        """
        Test that the _calculate_filter_length method returns the correct value.
        """
        assert filter_builder._calculate_filter_length(d) == N

    @pytest.mark.parametrize(
        "filter_conf",
        list(lowpass_filter_configurations),
    )
    def test_calculate_impulse_response_coefficients_raises_value_error(
        self, filter_builder: IFilter
    ):
        """
        Test that the calculate_impulse_response_coefficients method raises a ValueError.
        """
        with pytest.raises(ValueError):
            filter_builder.calculate_impulse_response_coefficients()

    @pytest.mark.parametrize(
        "filter_conf, order",
        list(zip(lowpass_filter_configurations, lowpass_order_results)),
    )
    def test_calculate_impulse_response_coefficients_returns_list(
        self, filter_builder: IFilter, order: tuple[int, int]
    ):
        """
        Test that the calculate_impulse_response_coefficients method returns a list.
        """
        n, N = order
        filter_builder.n = n
        assert isinstance(
            filter_builder.calculate_impulse_response_coefficients(), list
        )

    @pytest.mark.parametrize(
        "filter_conf, order",
        list(zip(lowpass_filter_configurations, lowpass_order_results)),
    )
    def test_calculate_impulse_response_coefficients_correct_length(
        self, filter_builder: IFilter, order: tuple[int, int], coefficients: list[float]
    ):
        """
        Test that the calculate_impulse_response_coefficients method returns the correct length.
        """
        n, N = order
        filter_builder.n = n
        c = filter_builder.calculate_impulse_response_coefficients()
        assert len(c) == n + 1

    @pytest.mark.parametrize(
        "filter_conf, order, coefficients",
        list(
            zip(
                lowpass_filter_configurations,
                lowpass_order_results,
                correct_impulse_response_coefficients,
            )
        ),
    )
    def test_calculate_impulse_response_coefficients_correct_values(
        self, filter_builder: IFilter, order: tuple[int, int], coefficients: list[float]
    ):
        """
        Test that the calculate_impulse_response_coefficients method returns the correct values.
        """
        n, N = order
        filter_builder.n = n
        c = filter_builder.calculate_impulse_response_coefficients()
        assert c == coefficients
