"""
This file contains the implementation of the easy_fir_filter class.
"""

import math

from easy_fir_filter.factory.filter_factory import FilterFactory
from easy_fir_filter.interfaces.easy_fir_filter_interface import IEasyFirFilter
from easy_fir_filter.types import FilterConf
from easy_fir_filter.utils import truncate, build_filter_coefficients
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
        self.fir_filter_coefficients: list[float] = []

    def calculate_filter(self) -> list[float]:

        # Delta
        self.calculate_delta()
        # Ripples A's and A'p
        self.calculate_ripples()
        # D parameter
        self.calculate_d_parameter()
        # Filter order
        n, N = self.filter.calculate_filter_order(self.D)       # type: ignore
        # Impulse response coefficients
        self.filter.calculate_impulse_response_coefficients()
        # Window coefficients
        if self.filter_conf["window_type"] == "kaiser":
            self.window.calculate_window_coefficients(n, N, self.AS) # type: ignore
        else:
            self.window.calculate_window_coefficients(n, N)
        # FIR filter coefficients
        self._calculate_filter_coefficients()

        return build_filter_coefficients(self.fir_filter_coefficients)

    def calculate_delta(self) -> float:
        # Tolerance allowed on the stopband ripple
        delta_s = 10 ** (-0.05 * self.As)
        # Tolerance allowed on the passband ripple
        delta_p = (10 ** (0.05 * self.Ap) - 1) / (10 ** (0.05 * self.Ap) + 1)

        min_delta = min(delta_s, delta_p)
        self.delta = truncate(min_delta, self.round_to)

        return self.delta

    def calculate_ripples(self) -> tuple[float, float]:
        if self.delta is None:
            raise ValueError("Delta must be calculated first. Call calculate_delta().")

        self.AS = truncate(-20 * math.log10(self.delta), self.round_to)
        self.AP = truncate(
            20 * math.log10((1 + self.delta) / (1 - self.delta)), self.round_to
        )
        return self.AS, self.AP

    def calculate_d_parameter(self) -> float:
        if self.AS is None or self.AP is None:
            raise ValueError(
                "AS and AP must be calculated first. Call calculate_ripples()."
            )

        self.D = (
            0.9222
            if self.AS <= 21
            else truncate((self.AS - 7.95) / 14.36, self.round_to)
        )
        return self.D

    def _calculate_filter_coefficients(self) -> list[float]:

        if self.window.window_coefficients is None:
            raise ValueError(
                "Window coefficients must be calculated first. Call calculate_window_coefficients()."
            )

        if self.filter.impulse_response_coefficients is None:
            raise ValueError(
                "Impulse response coefficients must be calculated first. Call calculate_impulse_response_coefficients()."
            )

        for i in range(self.filter.n + 1):
            self.fir_filter_coefficients.append(
                truncate(
                    self.window.window_coefficients[i]
                    * self.filter.impulse_response_coefficients[i],
                    self.round_to,
                )
            )

        return self.fir_filter_coefficients
