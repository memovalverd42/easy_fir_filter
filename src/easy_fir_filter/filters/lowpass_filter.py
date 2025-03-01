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
    sampling frequency, passband frequency, and stopband frequency. The filter
    uses the sinc function for the calculation of impulse response coefficients,
    which is a fundamental technique in FIR filter design. The sinc function represents
    the ideal impulse response of a lowpass filter, and by modifying its parameters,
    we can create lowpass filters.
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
        self.n: int | None = None
        self.impulse_response_coefficients: list[float] = []

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
        if not d:
            raise ValueError("The design parameter 'd' must be calculated first.")

        N = int(((self.F * d) / (self.fs - self.fp)) + self._FILTER_ORDER_FACTOR)
        return N

    def calculate_impulse_response_coefficients(self) -> list[float]:
        """
        Computes the impulse response coefficients of the low-pass filter.

        The method calculates the filter's impulse response using the sinc function,
        which is essential for designing FIR filters. The coefficients are rounded
        to the specified decimal precision.

        The formula used for calculating the coefficients is:
            c = n0 * (sin(term) / term)
        Where:
            fc = 0.5 * (fp + fs) (cut-off frequency)
            F = sampling frequency
            term = (2 * pi * nc * fc) / F
            nc = coefficient index
            n0 = (2 * fc) / F (Normalized frequency)

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
