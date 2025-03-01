"""
This file contains tests for the bandstop filter.
"""

import pytest

from easy_fir_filter import FilterConf
from easy_fir_filter.filters.bandstop_filter import BandstopFilter
from easy_fir_filter.filters.highpass_filter import HighpassFilter

bandstop_filter_configurations: list[FilterConf] = [
    {
        "filter_type": "bandstop",
        "window_type": "kaiser",
        "sampling_freq_hz": 13000,
        "passband_freq_hz": 2000,
        "stopband_freq_hz": 3000,
        "stopband_freq2_hz": 4000,
        "passband_freq2_hz": 5000,
        "passband_ripple_db": 0.2,
        "stopband_attenuation_db": 43,
    },
    {
        "filter_type": "bandstop",
        "window_type": "hamming",
        "sampling_freq_hz": 8000,
        "passband_freq_hz": 1000,
        "stopband_freq_hz": 1500,
        "stopband_freq2_hz": 2000,
        "passband_freq2_hz": 2500,
        "passband_ripple_db": 0.3,
        "stopband_attenuation_db": 50,
    },
    {
        "filter_type": "bandstop",
        "window_type": "blackman",
        "sampling_freq_hz": 44100,
        "passband_freq_hz": 5000,
        "stopband_freq_hz": 6000,
        "stopband_freq2_hz": 7000,
        "passband_freq2_hz": 8000,
        "passband_ripple_db": 0.1,
        "stopband_attenuation_db": 60,
    },
    {
        "filter_type": "bandstop",
        "window_type": "kaiser",
        "sampling_freq_hz": 16000,
        "passband_freq_hz": 500,
        "stopband_freq_hz": 750,
        "stopband_freq2_hz": 1000,
        "passband_freq2_hz": 1250,
        "passband_ripple_db": 0.4,
        "stopband_attenuation_db": 40,
    },
    {
        "filter_type": "bandstop",
        "window_type": "hamming",
        "sampling_freq_hz": 1000,
        "passband_freq_hz": 100,
        "stopband_freq_hz": 150,
        "stopband_freq2_hz": 200,
        "passband_freq2_hz": 250,
        "passband_ripple_db": 0.25,
        "stopband_attenuation_db": 35,
    },
    {
        "filter_type": "bandstop",
        "window_type": "blackman",
        "sampling_freq_hz": 96000,
        "passband_freq_hz": 10000,
        "stopband_freq_hz": 12000,
        "stopband_freq2_hz": 14000,
        "passband_freq2_hz": 16000,
        "passband_ripple_db": 0.05,
        "stopband_attenuation_db": 75,
    },
    {
        "filter_type": "bandstop",
        "window_type": "kaiser",
        "sampling_freq_hz": 6000,
        "passband_freq_hz": 200,
        "stopband_freq_hz": 300,
        "stopband_freq2_hz": 400,
        "passband_freq2_hz": 500,
        "passband_ripple_db": 0.15,
        "stopband_attenuation_db": 55,
    },
]

bandstop_d_results = [
    2.4408127,
    2.9282878,
    3.6246518,
    2.2318941,
    2.0117495,
    4.669315,
    3.2764894,
]

bandstop_N_results = [
    32,
    47,
    160,
    143,
    41,
    225,
    197,
]

bandstop_order_results = [
    (16, 33),
    (24, 49),
    (80, 161),
    (72, 145),
    (21, 43),
    (113, 227),
    (99, 199),
]

bandstop_coefficients_results = [
    [
        0.6923076923076923,
        0.035661,
        0.2543517,
        -0.0747008,
        -0.1317668,
        0.0479625,
        0.0190063,
        0.0162911,
        0.0299765,
        -0.058563,
        -0.0224102,
        0.0462457,
        0.0029717,
        0.0,
        -0.0025472,
        -0.0339135,
        0.0140064,
    ],
    [
        0.75,
        -0.0475286,
        0.2079459,
        0.1089213,
        -0.1125395,
        -0.0978074,
        0.0287113,
        0.0341346,
        0.0,
        0.0265491,
        0.0172268,
        -0.0444579,
        -0.0375131,
        0.0251357,
        0.0297065,
        -0.0031685,
        0.0,
        0.0027958,
        -0.0231051,
        -0.0171981,
        0.0225079,
        0.0232874,
        -0.0078303,
        -0.0103888,
        0.0,
    ],
    [
        0.909297052154195,
        -0.0543247,
        0.0248479,
        0.0822242,
        0.0726285,
        0.0068103,
        -0.0598327,
        -0.0748819,
        -0.0311377,
        0.0313655,
        0.0621407,
        0.0418596,
        -0.0061615,
        -0.0406579,
        -0.038194,
        -0.0087139,
        0.0190002,
        0.0246631,
        0.0110386,
        -0.0043972,
        -0.0086777,
        -0.0037331,
        -9.5e-06,
        -0.0028782,
        -0.007075,
        -0.0041381,
        0.0064511,
        0.0151587,
        0.011903,
        -0.0028003,
        -0.0169413,
        -0.0178193,
        -0.0041015,
        0.0126608,
        0.0185146,
        0.0094996,
        -0.0055846,
        -0.0139672,
        -0.0103085,
        -0.0001158,
        0.0069587,
        0.0063955,
        0.0016322,
        -0.0012119,
        -0.0002052,
        0.0012162,
        -0.0006945,
        -0.0048831,
        -0.006237,
        -0.0014501,
        0.006477,
        0.010329,
        0.0056603,
        -0.0043403,
        -0.0112575,
        -0.0090738,
        0.0002812,
        0.008769,
        0.0095994,
        0.0030497,
        -0.00452,
        -0.0069774,
        -0.0036946,
        0.0009756,
        0.0027385,
        0.0013975,
        2.85e-05,
        0.0008131,
        0.0024144,
        0.0017542,
        -0.0019504,
        -0.0055756,
        -0.004984,
        0.000437,
        0.0064546,
        0.0076159,
        0.0024626,
        -0.0048247,
        -0.0081036,
        -0.0048119,
        0.0018824,
    ],
    [
        0.9375,
        -0.058752,
        -0.0480033,
        -0.0316688,
        -0.0118821,
        0.0088067,
        0.0277878,
        0.0427494,
        0.0519864,
        0.0546134,
        0.0506537,
        0.0409963,
        0.0272303,
        0.0113865,
        -0.0043714,
        -0.0180586,
        -0.0281348,
        -0.0336897,
        -0.0345211,
        -0.0311026,
        -0.0244518,
        -0.0159264,
        -0.0069843,
        0.0010498,
        0.0071778,
        0.0108488,
        0.011997,
        0.0109945,
        0.0085336,
        0.0054658,
        0.0026263,
        0.0006781,
        0.0,
        0.000637,
        0.0023173,
        0.0045288,
        0.0066372,
        0.008023,
        0.0082085,
        0.0069543,
        0.0043067,
        0.0005889,
        -0.0036584,
        -0.007778,
        -0.0111144,
        -0.0131322,
        -0.0135082,
        -0.0121856,
        -0.0093782,
        -0.0055281,
        -0.001224,
        0.0029024,
        0.0062839,
        0.0085086,
        0.0093803,
        0.0089367,
        0.0074266,
        0.0052499,
        0.0028746,
        0.0007463,
        -0.0007921,
        -0.0015574,
        -0.0015484,
        -0.0009325,
        0.0,
        0.0009038,
        0.0014546,
        0.001418,
        0.0006989,
        -0.0006381,
        -0.0023818,
        -0.0042147,
        -0.0057762,
    ],
    [
        0.8,
        -0.0893118,
        0.1099733,
        0.169565,
        0.0467744,
        -0.0900316,
        -0.0959713,
        -0.0115099,
        0.0378413,
        0.019476,
        0.0,
        0.0159349,
        0.0252275,
        -0.0061976,
        -0.0411305,
        -0.0300105,
        0.0116936,
        0.0299232,
        0.0122192,
        -0.0047006,
        0.0,
        0.0042529,
    ],
    [
        0.9166666666666666,
        -0.0547887,
        0.0107533,
        0.0675219,
        0.0768659,
        0.0342817,
        -0.0287113,
        -0.0683229,
        -0.0596831,
        -0.0127493,
        0.0374344,
        0.0572565,
        0.0375131,
        -0.0031754,
        -0.0348467,
        -0.0384572,
        -0.017229,
        0.0095498,
        0.0231051,
        0.0182938,
        0.0041192,
        -0.0064452,
        -0.0074254,
        -0.0027162,
        0.0,
        -0.0024989,
        -0.006283,
        -0.0050129,
        0.0029423,
        0.0119856,
        0.013863,
        0.005237,
        -0.0086145,
        -0.0174805,
        -0.0143486,
        -0.0011794,
        0.0125043,
        0.0170222,
        0.0098511,
        -0.0029421,
        -0.0119366,
        -0.0116648,
        -0.0041016,
        0.0039862,
        0.0069878,
        0.0045014,
        0.0004675,
        -0.0011657,
        0.0,
        0.0011181,
        -0.0004301,
        -0.0039718,
        -0.0059127,
        -0.0032341,
        0.0031901,
        0.0086956,
        0.0085261,
        0.002013,
        -0.0064542,
        -0.0106749,
        -0.0075026,
        0.0006767,
        0.0078686,
        0.0091564,
        0.0043072,
        -0.0024976,
        -0.0063013,
        -0.0051878,
        -0.0012115,
        0.0019615,
        0.0023337,
        0.0008799,
        0.0,
        0.0008558,
        0.0022075,
        0.0018046,
        -0.001084,
        -0.004514,
        -0.0053319,
        -0.002055,
        0.0034458,
        0.0071217,
        0.0059494,
        0.0004973,
        -0.005359,
        -0.0074096,
        -0.0043528,
        0.0013189,
        0.0054257,
        0.0053737,
        0.001914,
        -0.0018836,
        -0.0033419,
        -0.0021781,
        -0.0002287,
        0.0005767,
        0.0,
        -0.0005648,
        0.0002194,
        0.0020461,
        0.0030746,
        0.0016971,
        -0.0016889,
        -0.0046433,
        -0.004591,
        -0.0010928,
        0.0035315,
        0.0058861,
        0.0041681,
        -0.0003787,
        -0.004435,
        -0.0051969,
        -0.0024612,
        0.0014367,
    ],
    [
        0.9333333333333333,
        -0.062125,
        -0.0491815,
        -0.0297706,
        -0.0067665,
        0.0164769,
        0.0366577,
        0.0510369,
        0.0578452,
        0.0565216,
        0.0477464,
        0.0332728,
        0.0155914,
        -0.0025069,
        -0.0183941,
        -0.0300105,
        -0.0361496,
        -0.0365796,
        -0.0319904,
        -0.023788,
        -0.0137832,
        -0.0038366,
        0.004471,
        0.0100872,
        0.0126137,
        0.0122985,
        0.0099045,
        0.006492,
        0.003163,
        0.0008223,
        0.0,
        0.0007692,
        0.0027677,
        0.0053116,
        0.007574,
        0.0087846,
        0.0084091,
        0.0062704,
        0.0025885,
        -0.0020658,
        -0.0068916,
        -0.0110237,
        -0.0137101,
        -0.0144617,
        -0.0131453,
        -0.0100035,
        -0.0055982,
        -0.0006934,
        0.0038978,
        0.0074694,
        0.0095492,
        0.0099744,
        0.0088992,
        0.0067407,
        0.004073,
        0.0014979,
        -0.0004833,
        -0.0015668,
        -0.0016959,
        -0.0010529,
        0.0,
        0.0010184,
        0.0015865,
        0.0014176,
        0.0004229,
        -0.0012674,
        -0.0033325,
        -0.0053322,
        -0.0068053,
        -0.0073723,
        -0.0068209,
        -0.0051549,
        -0.0025985,
        0.0004464,
        0.0034799,
        0.0060021,
        0.0076104,
        0.008076,
        0.0073824,
        0.0057211,
        0.0034458,
        0.0009946,
        -0.0011995,
        -0.0027952,
        -0.0036039,
        -0.0036172,
        -0.0029943,
        -0.0020147,
        -0.0010064,
        -0.0002679,
        0.0,
        -0.000262,
        -0.0009626,
        -0.0018847,
        -0.0027395,
        -0.0032364,
        -0.0031534,
        -0.0023918,
        -0.0010037,
        0.0008138,
    ],
]


class TestBandstopFilter:
    """
    Bandstop Filter Tests
    """

    @pytest.fixture
    def filter_builder(self, filter_conf: FilterConf, round_to: int = 7):
        """
        Returns a Bandstop object.
        """
        return BandstopFilter(filter_conf, round_to)

    @pytest.mark.parametrize(
        "filter_conf, d",
        list(zip(bandstop_filter_configurations, bandstop_d_results)),
    )
    def test_calculate_filter_length_returns_int(
        self, filter_builder: HighpassFilter, d: float
    ):
        """
        Test that the _calculate_filter_length method returns an integer.
        """
        assert isinstance(filter_builder._calculate_filter_length(d), int)

    @pytest.mark.parametrize("filter_conf", bandstop_filter_configurations)
    def test_calculate_filter_length_raises_value_error(
        self, filter_builder: HighpassFilter
    ):
        """
        Test that the _calculate_filter_length method raises a ValueError if d is not provided.
        """
        with pytest.raises(ValueError):
            filter_builder._calculate_filter_length(None)

    @pytest.mark.parametrize(
        "filter_conf, d, expected_N",
        list(
            zip(bandstop_filter_configurations, bandstop_d_results, bandstop_N_results)
        ),
    )
    def test_calculate_filter_length_correct_value(
        self, filter_builder: HighpassFilter, d: float, expected_N: int
    ):
        """
        Test that the _calculate_filter_length method returns the correct value.
        """
        assert filter_builder._calculate_filter_length(d) == expected_N

    @pytest.mark.parametrize(
        "filter_conf",
        bandstop_filter_configurations,
    )
    def test_calculate_impulse_response_coefficients_raises_value_error(
        self, filter_builder: HighpassFilter
    ):
        """
        Test that the calculate_impulse_response_coefficients method raises a ValueError
        if self.n is not previously calculate.
        """
        with pytest.raises(ValueError):
            filter_builder.calculate_impulse_response_coefficients()

    @pytest.mark.parametrize(
        "filter_conf, order",
        list(zip(bandstop_filter_configurations, bandstop_order_results)),
    )
    def test_calculate_impulse_response_coefficients_returns_list(
        self, filter_builder: HighpassFilter, order: tuple[int, int]
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
        list(zip(bandstop_filter_configurations, bandstop_order_results)),
    )
    def test_calculate_impulse_response_coefficients_correct_length(
        self, filter_builder: HighpassFilter, order: tuple[int, int]
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
                bandstop_filter_configurations,
                bandstop_order_results,
                bandstop_coefficients_results,
            )
        ),
    )
    def test_calculate_impulse_response_coefficients_correct_values(
        self,
        filter_builder: HighpassFilter,
        order: tuple[int, int],
        coefficients: list[float],
    ):
        """
        Test that the calculate_impulse_response_coefficients method returns the correct values.
        """
        n, N = order
        filter_builder.n = n
        c = filter_builder.calculate_impulse_response_coefficients()
        assert c == coefficients
