"""
This file contains the implementation of the easy_fir_filter class.
"""

import math

from easy_fir_filter.factory.filter_factory import FilterFactory
from easy_fir_filter.interfaces.easy_fir_filter_interface import IEasyFirFilter
from easy_fir_filter.types import FilterConf
from easy_fir_filter.validators.filter_conf_validator import FilterConfValidator


class EasyFirFilter(IEasyFirFilter, FilterConfValidator):
    """
    Easy Filter Class
    """

    def __init__(self, filter_conf: FilterConf, round_to: int = 4):
        """
        Constructor
        """
        FilterConfValidator.__init__(self, filter_conf)

        self.round_to = round_to
        self.filter_conf = filter_conf

        self.filter = FilterFactory.create_filter(filter_conf, round_to)
        self.window = FilterFactory.create_window(filter_conf["window_type"], round_to)

        self.As = filter_conf["stopband_attenuation_db"]
        self.Ap = filter_conf["passband_ripple_db"]

        self.delta = None
        self.AP = None
        self.AS = None
        self.D = None

    def calculate_filter(self) -> list[float]:
        return []

    def calculate_delta(self) -> float:
        # Tolerance allowed on the stopband ripple
        delta_s = 10 ** (-0.05 * self.As)
        # Tolerance allowed on the passband ripple
        delta_p = (10 ** (0.05 * self.Ap) - 1) / (10 ** (0.05 * self.Ap) + 1)

        self.delta = round(min(delta_s, delta_p), self.round_to)
        return self.delta

    def calculate_ripples(self) -> tuple[float, float]:
        if self.delta is None:
            raise ValueError("Delta must be calculated first. Call calculate_delta().")

        self.AS = round(-20 * math.log10(self.delta), self.round_to)
        self.AP = round(
            20 * math.log10((1 + self.delta) / (1 - self.delta)), self.round_to
        )
        return self.AS, self.AP

    def calculate_d_parameter(self) -> float:
        if self.AS is None or self.AP is None:
            raise ValueError(
                "AS and AP must be calculated first. Call calculate_ripples()."
            )

        self.D = (
            0.9222 if self.AS <= 21 else round((self.AS - 7.95) / 14.36, self.round_to)
        )
        return self.D

    def calculate_filter_order(self) -> tuple[int, int]:
        return 0, 0

    def _calculate_filter_coefficients(self) -> list[float]:
        return []
