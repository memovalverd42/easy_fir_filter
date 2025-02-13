"""
This module contains the implementation of the Highpass FIR Filter class.
"""

import math
from easy_fir_filter.types.fir_filter_conf import FilterConf
from easy_fir_filter.interfaces.filter_interface import IFilter
from easy_fir_filter.utils import truncate


class HighpassFilter(IFilter):
    """
    Implementation of a Highpass FIR filter.

    This class designs a highpass FIR filter based on the given filter configuration.
    The filter uses the sinc function for the calculation of impulse response coefficients.
    """

    _FILTER_ORDER_FACTOR = 1

    def __init__(self, filter_conf: FilterConf, round_to: int = 4):
        """
        Initializes the highpass filter with the given configuration.

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

        The length of the filter is determined using the sampling frequency and
        the difference between the passband and stopband frequencies.

        Args:
            d (float): The D parameter, used for determining the required filter length.

        Returns:
            int: Computed filter length (N).
        """
        N = int(((self.F * d) / (self.fp - self.fs)) + self._FILTER_ORDER_FACTOR)
        return N

    def calculate_impulse_response_coefficients(self) -> list[float]:
        """
        Computes the impulse response coefficients of the highpass filter.

        The method calculates the filter's impulse response using the sinc function,
        which is essential for designing FIR filters. The coefficients are rounded
        to the specified decimal precision.

        Returns:
            list[float]: The list of computed impulse response coefficients.

        Raises:
            ValueError: If the filter order has not been calculated before calling this method.
        """
        if self.n is None:
            raise ValueError("Order must be calculated first. Call calculate_order().")

        nc = 1
        fc = 0.5 * (self.fp + self.fs)
        n0 = 1 - ((2 * fc) / self.F)
        self.impulse_response_coefficients.append(truncate(n0, self.round_to))

        while nc <= self.n:
            term = (2 * math.pi * nc * fc) / self.F
            c = -((2 * fc) / self.F) * (math.sin(term) / term)
            nc += 1
            self.impulse_response_coefficients.append(truncate(c, self.round_to))

        return self.impulse_response_coefficients
