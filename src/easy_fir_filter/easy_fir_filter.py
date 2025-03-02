"""
This module contains the implementation of the EasyFirFilter class, which provides a high-level interface
for designing and calculating FIR filter coefficients based on a given filter configuration.
"""

import math

from easy_fir_filter.factory.filter_factory import FilterFactory
from easy_fir_filter.interfaces.easy_fir_filter_interface import IEasyFirFilter
from easy_fir_filter.types import FilterConf
from easy_fir_filter.utils import build_filter_coefficients, truncate
from easy_fir_filter.validators.filter_conf_validator import \
    FilterConfValidator


class EasyFirFilter(IEasyFirFilter, FilterConfValidator):
    """
    EasyFirFilter Class: Provides a simplified interface for designing FIR filters.

    This class encapsulates the process of calculating FIR filter coefficients based on a provided
    filter configuration. It handles validation, filter creation, windowing, and coefficient calculation.

    Attributes:
        filter_conf (FilterConf): The filter configuration dictionary.
        round_to (int): The number of decimal places to round coefficients to.
        filter: The filter object created by FilterFactory.
        window: The window object created by FilterFactory.
        As (float): Stopband attenuation in dB.
        Ap (float): Passband ripple in dB.
        delta (float): Minimum tolerance between passband and stopband ripples.
        AP (float): Calculated passband ripple.
        AS (float): Calculated stopband attenuation.
        D (float): Kaiser window parameter.
        fir_filter_coefficients (list[float]): The calculated FIR filter coefficients.
    """

    def __init__(self, filter_conf: FilterConf, round_to: int = 4):
        """
        Initializes the EasyFirFilter with the given filter configuration and rounding precision.

        Args:
            filter_conf (FilterConf): The filter configuration dictionary.
            round_to (int): The number of decimal places to round coefficients to (default: 4).
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
        """
        Calculates the FIR filter coefficients based on the filter configuration.

        This method orchestrates the entire filter design process, including delta calculation,
        ripple calculation, D parameter calculation, filter order calculation, impulse response calculation,
        windowing, and final coefficient calculation.

        Returns:
            list[float]: The calculated FIR filter coefficients.
        """
        # Delta
        self.calculate_delta()
        # Ripples A's and Ap
        self.calculate_ripples()
        # D parameter
        self.calculate_d_parameter()
        # Filter order
        n, N = self.filter.calculate_filter_order(self.D)  # type: ignore
        # Impulse response coefficients
        self.filter.calculate_impulse_response_coefficients()
        # Window coefficients
        if self.filter_conf["window_type"] == "kaiser":
            self.window.calculate_window_coefficients(n, N, self.AS)  # type: ignore
        else:
            self.window.calculate_window_coefficients(n, N)
        # FIR filter coefficients
        self._calculate_filter_coefficients()

        return build_filter_coefficients(self.fir_filter_coefficients)

    def calculate_delta(self) -> float:
        """
        Calculates the minimum tolerance (delta) between passband and stopband ripples.

        Returns:
            float: The calculated delta value.
        """
        # Tolerance allowed on the stopband ripple
        delta_s = 10 ** (-0.05 * self.As)
        # Tolerance allowed on the passband ripple
        delta_p = (10 ** (0.05 * self.Ap) - 1) / (10 ** (0.05 * self.Ap) + 1)

        min_delta = min(delta_s, delta_p)
        self.delta = truncate(min_delta, self.round_to)

        return self.delta

    def calculate_ripples(self) -> tuple[float, float]:
        """
        Calculates the passband and stopband ripples (AP and AS) based on the delta value.

        Returns:
            tuple[float, float]: The calculated AS and AP values.

        Raises:
            ValueError: If delta has not been calculated yet.
        """
        if self.delta is None:
            raise ValueError("Delta must be calculated first. Call calculate_delta().")

        self.AS = truncate(-20 * math.log10(self.delta), self.round_to)
        self.AP = truncate(
            20 * math.log10((1 + self.delta) / (1 - self.delta)), self.round_to
        )
        return self.AS, self.AP

    def calculate_d_parameter(self) -> float:
        """
        Calculates the D parameter for the Kaiser window.

        Returns:
            float: The calculated D parameter.

        Raises:
            ValueError: If AS or AP have not been calculated yet.
        """
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
        """
        Calculates the final FIR filter coefficients by multiplying the impulse response and window coefficients.

        Returns:
            list[float]: The calculated FIR filter coefficients.

        Raises:
            ValueError: If window or impulse response coefficients have not been calculated yet.
        """
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
        print(self.fir_filter_coefficients)
        return self.fir_filter_coefficients
