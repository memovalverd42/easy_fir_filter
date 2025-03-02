"""
This file contains the implementation of the BandpassFilter class.
"""

import math

from easy_fir_filter.interfaces.filter_interface import IFilter
from easy_fir_filter.types.fir_filter_conf import FilterConf
from easy_fir_filter.utils import truncate


class BandpassFilter(IFilter):
    """
    Implementation of a Bandpass FIR filter.

    This class designs a bandpass FIR filter using the sinc function.
    The filter allows frequencies between two cutoff frequencies to pass.
    The bandpass filter is created by combining two sinc functions, one for the
    lower cutoff frequency and one for the upper cutoff frequency, resulting in
    a filter that passes frequencies within a specific band.
    """

    _FILTER_ORDER_FACTOR = 1

    def __init__(self, filter_conf: FilterConf, round_to: int = 4):
        """
        Initializes the bandpass filter with the given configuration.

        Args:
            filter_conf (FilterConf): Configuration containing:
                - sampling_freq_hz (float): Sampling frequency in Hz.
                - passband_freq_hz (float): Lower passband frequency in Hz.
                - stopband_freq_hz (float): Lower stopband frequency in Hz.
                - passband_freq2_hz (float): Upper passband frequency in Hz.
                - stopband_freq2_hz (float): Upper stopband frequency in Hz.
            round_to (int, optional): Number of decimal places for rounding coefficients. Defaults to 4.
        """
        self.n: int | None = None
        self.impulse_response_coefficients: list[float] = []

        self.filter_conf = filter_conf
        self.round_to = round_to

        self.F = filter_conf["sampling_freq_hz"]
        self.fp = filter_conf["passband_freq_hz"]
        self.fs = filter_conf["stopband_freq_hz"]
        self.fp2 = filter_conf.get("passband_freq2_hz", None)
        self.fs2 = filter_conf.get("stopband_freq2_hz", None)

    def _calculate_filter_length(self, d: float):
        """
        Calculates and sets the filter order based on transition bandwidth.

        Args:
            d (float): Parameter D, used to determine the required filter length.
        """
        if not d:
            raise ValueError("The design parameter 'd' must be calculated first.")

        N = math.ceil(
            ((self.F * d) / min(self.fp - self.fs, self.fs2 - self.fp2))
            + self._FILTER_ORDER_FACTOR
        )

        return int(N)

    def calculate_impulse_response_coefficients(self) -> list[float]:
        """
        Computes the impulse response coefficients of the bandpass filter.

        The formula used for calculating the coefficients is:
            c = (1 / (nc * pi)) * (sin(term1) - sin(term2))
        Where:
            term1 = (2 * pi * nc * fc2) / F
            term2 = (2 * pi * nc * fc1) / F
            fc1 = fp - (deltaF / 2) (lower cutoff frequency)
            fc2 = fp2 + (deltaF / 2) (upper cutoff frequency)
            F = sampling frequency
            nc = coefficient index

        Returns:
            list[float]: The computed impulse response coefficients.

        Raises:
            ValueError: If the filter order has not been calculated first.
        """
        if self.n is None:
            raise ValueError("Order must be calculated first. Call calculate_order().")

        nc = 1
        deltaF = min(self.fp - self.fs, self.fs2 - self.fp2)
        fc1 = self.fp - (deltaF / 2)
        fc2 = self.fp2 + (deltaF / 2)

        n0 = (2 / self.F) * (fc2 - fc1)
        self.impulse_response_coefficients.append(truncate(n0, self.round_to))

        while nc <= self.n:
            term1 = (2 * math.pi * nc * fc2) / self.F
            term2 = (2 * math.pi * nc * fc1) / self.F
            c = (1 / (nc * math.pi)) * (math.sin(term1) - math.sin(term2))
            self.impulse_response_coefficients.append(truncate(c, self.round_to))
            nc += 1

        return self.impulse_response_coefficients
