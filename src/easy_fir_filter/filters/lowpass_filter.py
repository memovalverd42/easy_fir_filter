"""
This module contains the implementation of the LowpassFilter class.
"""

import math
from easy_fir_filter.types.fir_filter_conf import FilterConf
from easy_fir_filter.interfaces.filter_interface import IFilter
from easy_fir_filter.utils import truncate


class LowpassFilter(IFilter):
    """
    Implementation of a Low-pass FIR filter.

    This class designs a low-pass filter based on given specifications such as
    sampling frequency, passband frequency, and stopband frequency.
    """

    _FILTER_ORDER_FACTOR = 1

    def __init__(self, filter_conf: FilterConf, round_to: int = 4):
        """
        Initializes the low-pass filter with the given configuration.

        Args:
            filter_conf (FilterConf): Configuration containing:
                - sampling_freq_hz (float): Sampling frequency in Hz.
                - passband_freq_hz (float): Passband frequency in Hz.
                - stopband_freq_hz (float): Stopband frequency in Hz.
            round_to (int, optional): Number of decimal places for rounding the
                                      impulse response coefficients. Defaults to 4.
        """
        self.filter_conf = filter_conf
        self.round_to = round_to

        self.F = filter_conf["sampling_freq_hz"]
        self.fp = filter_conf["passband_freq_hz"]
        self.fs = filter_conf["stopband_freq_hz"]

    def _calculate_filter_length(self, d: float) -> int:
        """
        Calculates the filter length (N) based on the transition bandwidth.

        Args:
            d (float): The D parameter, used for determining the required filter length.

        Returns:
            int: Computed filter length (N).
        """
        N = int(((self.F * d) / (self.fs - self.fp)) + self._FILTER_ORDER_FACTOR)
        return N

    def calculate_impulse_response_coefficients(self) -> list[float]:
        """
        Computes the impulse response coefficients of the low-pass filter.

        The method calculates the filter's impulse response using the sinc function,
        which is essential for designing FIR filters.

        Returns:
            list[float]: The list of computed impulse response coefficients.

        Raises:
            ValueError: If the filter order has not been calculated before calling this method.
        """
        if self.n is None:
            raise ValueError("Order must be calculated first. Call calculate_order().")

        nc = 1
        fc = 0.5 * (self.fp + self.fs)  # Cutoff frequency
        n0 = (2 * fc) / self.F  # Normalized frequency
        self.impulse_response_coefficients.append(n0)

        while nc <= self.n:
            term = (2 * math.pi * nc * fc) / self.F
            c = n0 * ((math.sin(term)) / term)
            nc += 1
            self.impulse_response_coefficients.append(truncate(c, self.round_to))

        return self.impulse_response_coefficients
