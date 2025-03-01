"""
This file contains the tests for the Kaiser window implementation.
"""

from unittest.mock import patch

import pytest

from easy_fir_filter import FilterConf
from easy_fir_filter.windows.kaiser_window import KaiserWindow
from tests.fixtures.filter_configurations import (
    filter_order_results,
    ripples_results,
)

kaiser_filter_configurations: list[FilterConf] = [
    {
        "filter_type": "highpass",
        "window_type": "kaiser",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 34,
    },
    {
        "filter_type": "lowpass",
        "window_type": "kaiser",
        "sampling_freq_hz": 2500,
        "passband_freq_hz": 500,
        "stopband_freq_hz": 750,
        "passband_ripple_db": 0.1,
        "stopband_attenuation_db": 44,
    },
    {
        "filter_type": "highpass",
        "window_type": "kaiser",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_ripple_db": 0.3,
        "stopband_attenuation_db": 35,
    },
    {
        "filter_type": "bandstop",
        "window_type": "kaiser",
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
        "window_type": "kaiser",
        "sampling_freq_hz": 80,
        "passband_freq_hz": 16,
        "stopband_freq_hz": 8,
        "passband_freq2_hz": 24,
        "stopband_freq2_hz": 32,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 34,
    },
]

correct_window_coefficients = [
    [
        1.0,
        0.9896703,
        0.9591131,
        0.909601,
        0.8431828,
        0.7625777,
        0.671038,
        0.5721842,
        0.4698245,
        0.3677679,
        0.2696403,
    ],
    [
        1.0,
        0.9899626,
        0.9603086,
        0.9123848,
        0.8483462,
        0.7710283,
        0.6837801,
        0.5902701,
        0.4942773,
        0.3994818,
        0.3092683,
        0.2265542,
        0.153655,
        0.0921911,
    ],
    [
        1.0,
        0.9888476,
        0.9559032,
        0.9026737,
        0.831576,
        0.7457993,
        0.6491255,
        0.545719,
        0.4398968,
        0.335896,
        0.2376502,
    ],
    [
        1.0,
        0.9937727,
        0.9752649,
        0.9449921,
        0.9037922,
        0.8527962,
        0.7933867,
        0.7271485,
        0.6558136,
        0.5811992,
        0.5051469,
        0.4294595,
        0.3558426,
        0.2858509,
        0.2208412,
        0.1619353,
        0.1099918,
    ],
    [
        1.0,
        0.9896703,
        0.9591131,
        0.909601,
        0.8431828,
        0.7625777,
        0.671038,
        0.5721842,
        0.4698245,
        0.3677679,
        0.2696403,
    ],
]

correct_betas = [
    [
        2.6549984,
        2.64169,
        2.6013565,
        2.532707,
        2.4333462,
        2.299296,
        2.1239987,
        1.8960481,
        1.592999,
        1.1572869,
        0.0,
    ],
    [
        3.9523743,
        3.9406635,
        3.9053205,
        3.8456938,
        3.7606284,
        3.6483455,
        3.506231,
        3.3304685,
        3.115368,
        2.8520428,
        2.5254528,
        2.1063732,
        1.5201439,
        0.0,
    ],
    [
        2.8152136,
        2.8011021,
        2.7583347,
        2.6855426,
        2.5801858,
        2.4380464,
        2.2521708,
        2.0104646,
        1.6891281,
        1.2271231,
        0.0,
    ],
    [
        3.7464772,
        3.7391527,
        3.7170926,
        3.6800319,
        3.6275109,
        3.5588452,
        3.4730773,
        3.3689012,
        3.2445444,
        3.0975771,
        2.9245928,
        2.7206332,
        2.4780617,
        2.1840508,
        1.8137554,
        1.3037188,
        0.0,
    ],
    [
        2.6549984,
        2.64169,
        2.6013565,
        2.532707,
        2.4333462,
        2.299296,
        2.1239987,
        1.8960481,
        1.592999,
        1.1572869,
        0.0,
    ],
]

i_alpha_results = [
    [
        3.7086433999999997,
        3.7086433999999997,
        3.6703342999999995,
        3.5570085000000002,
        3.3733859,
        3.1270643999999996,
        2.8281288,
        2.4886407999999998,
        2.1220273,
        1.7424118,
        1.3639203,
    ],
    [
        10.847025299999999,
        10.847025299999999,
        10.738149899999998,
        10.416492400000001,
        9.896662,
        9.2020337,
        8.3633645,
        7.4169804,
        6.4026752,
        5.3614388,
        4.3331900999999995,
        3.3546413,
        2.4574399,
        1.6666998,
    ],
    [
        4.2078646,
        4.2078646,
        4.160937200000001,
        4.0223113,
        3.7983289,
        3.4991594,
        3.1382225,
        2.7314324999999995,
        2.2963119,
        1.8510265000000001,
        1.413405,
    ],
    [
        9.091581600000001,
        9.091581600000001,
        9.0349664,
        8.8667013,
        8.591472800000002,
        8.2169013,
        7.753267099999998,
        7.213140100000001,
        6.6109306,
        5.9623829,
        5.284020399999999,
        4.592584499999999,
        3.9044661,
        3.2351721,
        2.5988369000000002,
        2.0077966,
        1.4722484,
    ],
    [
        3.7086433999999997,
        3.7086433999999997,
        3.6703342999999995,
        3.5570085000000002,
        3.3733859,
        3.1270643999999996,
        2.8281288,
        2.4886407999999998,
        2.1220273,
        1.7424118,
        1.3639203,
    ],
]

# Values of AS for the tests
# contains AS < 21, 21 < AS <= 50, and AS > 50
AS_values = [20, 44, 35, 43, 51]
alpha_parameters = [0.0, 3.8614156, 2.7828933, 3.7464690, 4.66146]


class TestKaiserWindow:
    """
    Test the Kaiser window implementation.
    """

    @pytest.fixture
    def window_builder(self) -> KaiserWindow:
        """
        Fixture for the Kaiser window builder.
        """
        return KaiserWindow(round_to=7)

    @pytest.mark.parametrize("AS", AS_values)
    def test_calculate_alpha_parameter_must_return_float(
        self, window_builder: KaiserWindow, AS: float
    ):
        """
        Test the calculation of the alpha parameter.
        """
        assert isinstance(window_builder._calculate_alpha_parameter(AS), float)

    def test_calculate_alpha_parameter_must_raise_exception(
        self, window_builder: KaiserWindow
    ):
        """
        Test the calculation of the alpha parameter.
        """
        with pytest.raises(ValueError):
            window_builder._calculate_alpha_parameter(None)  # type: ignore

    def test_calculate_alpha_parameter_must_set_alpha_result_on_instance(
        self, window_builder: KaiserWindow
    ):
        """
        Test the calculation of the alpha parameter. The result must be set on the instance.
        """
        window_builder._calculate_alpha_parameter(44)
        assert window_builder.alpha == 3.8614156

    @pytest.mark.parametrize("AS, alpha", zip(AS_values, alpha_parameters))
    def test_calculate_alpha_parameter_must_return_correct_values(
        self, window_builder: KaiserWindow, AS: float, alpha: float
    ):
        """
        Test the calculation of the alpha parameter.
        """
        assert window_builder._calculate_alpha_parameter(AS) == alpha

    def test_calculate_betas_must_raise_exception(self, window_builder: KaiserWindow):
        """
        Test the calculation of the betas. It must raise an exception if the alpha parameter is not set.
        """
        with pytest.raises(ValueError):
            window_builder._calculate_betas(7, 8)

    def test_calculate_betas_must_return_list(self, window_builder: KaiserWindow):
        """
        Test the calculation of the betas. It must return a list of floats.
        """
        window_builder.alpha = 3.8614156
        assert isinstance(window_builder._calculate_betas(10, 21), list)

    @pytest.mark.parametrize(
        "ripples, filter_order",
        list(zip(ripples_results, filter_order_results)),
    )
    def test_calculate_betas_must_return_list_of_correct_length(
        self,
        window_builder: KaiserWindow,
        ripples: tuple[float, float],
        filter_order: tuple[int, int],
    ):
        """
        Test the calculation of the betas. It must return a list of floats.
        """
        n, N = filter_order
        window_builder._calculate_alpha_parameter(ripples[0])
        assert len(window_builder._calculate_betas(n, N)) == n + 1

    @pytest.mark.parametrize(
        "ripples, filter_order, betas",
        list(zip(ripples_results, filter_order_results, correct_betas)),
    )
    def test_calculate_betas_must_return_correct_values(
        self,
        window_builder: KaiserWindow,
        ripples: tuple[float, float],
        filter_order: tuple[int, int],
        betas: list[float],
    ):
        """
        Test the calculation of the betas. It must return a list of floats.
        """
        n, N = filter_order
        window_builder._calculate_alpha_parameter(ripples[0])
        assert window_builder._calculate_betas(n, N) == betas

    def test_calculate_i_alpha_must_raise_exception(self, window_builder: KaiserWindow):
        """
        Test the calculation of the i_alpha. It must raise an exception if the alpha parameter is not set.
        """
        with pytest.raises(ValueError):
            window_builder._calculate_i_alpha(None)  # type: ignore

    @pytest.mark.parametrize(
        "ripples",
        ripples_results,
    )
    def test_calculate_i_alpha_must_return_float(
        self,
        window_builder: KaiserWindow,
        ripples: tuple[float, float],
    ):
        """
        Test the calculation of the i_alpha. It must return a float.
        """
        window_builder._calculate_alpha_parameter(ripples[0])
        assert isinstance(
            window_builder._calculate_i_alpha(window_builder.alpha), float
        )

    def test_calculate_i_alpha_must_return_correct_value(
        self,
        window_builder: KaiserWindow,
    ):
        """
        Test the calculation of the i_alpha. It must return a float.
        """
        window_builder._calculate_alpha_parameter(ripples_results[0][0])
        assert (
            window_builder._calculate_i_alpha(window_builder.alpha)
            == i_alpha_results[0][0]
        )

    def test_calculate_window_coefficients_must_raise_exception(
        self, window_builder: KaiserWindow
    ):
        """
        Test the calculation of the window coefficients. It must raise an exception if the alpha parameter is not set.
        """
        # If n or N is not provided
        with pytest.raises(ValueError):
            window_builder.calculate_window_coefficients(None, None)  # type: ignore

        # If AS is not provided
        with pytest.raises(ValueError):
            window_builder.calculate_window_coefficients(7, 8)  # type: ignore

    def test_calculate_alpha_parameter_must_be_called_before_calculate_window_coefficients(
        self, window_builder: KaiserWindow
    ):
        def side_effect(AS):
            window_builder.alpha = 1.0
            return 1.0

        with patch.object(
            window_builder, "_calculate_alpha_parameter", side_effect=side_effect
        ) as mock_alpha:
            window_builder.calculate_window_coefficients(10, 21, 34)
            mock_alpha.assert_called_once_with(AS=34)

    def test_calculate_betas_must_be_called_before_calculate_window_coefficients(
        self, window_builder: KaiserWindow
    ):
        """
        Test the calculation of the window coefficients. The method must call the _calculate_betas method.
        """

        def alpha_side_effect(AS):
            window_builder.alpha = 1.0
            return 1.0

        with patch.object(
            window_builder, "_calculate_alpha_parameter", side_effect=alpha_side_effect
        ):
            with patch.object(window_builder, "_calculate_betas") as mock_betas:
                window_builder.calculate_window_coefficients(10, 21, 34)
                mock_betas.assert_called_once_with(n=10, filter_length=21)

    def test_calculate_window_coefficients_must_return_list(
        self, window_builder: KaiserWindow
    ):
        """
        Test the calculation of the window coefficients. It must return a list of floats.
        """
        window_builder.alpha = 1.0
        window_builder.betas = [1.0, 2.0, 3.0]
        assert isinstance(
            window_builder.calculate_window_coefficients(10, 21, 34), list
        )

    @pytest.mark.parametrize(
        "ripples, filter_order, window_coefficients",
        list(zip(ripples_results, filter_order_results, correct_window_coefficients)),
    )
    def test_calculate_window_coefficients_must_return_correct_values(
        self,
        window_builder: KaiserWindow,
        ripples: tuple[float, float],
        filter_order: tuple[int, int],
        window_coefficients: list[float],
    ):
        """
        Test the calculation of the window coefficients. It must return a list of floats.
        """
        n, N = filter_order
        AS, _ = ripples

        assert (
            window_builder.calculate_window_coefficients(n, N, AS)
            == window_coefficients
        )
