"""
This file contains the implementation of the BandstopFilter class.
"""

import math

from easy_fir_filter.types.fir_filter_conf import FilterConf
from easy_fir_filter.interfaces.filter_interface import IFilter
from easy_fir_filter.utils import truncate


class BandstopFilter(IFilter):
    """
    Implementation of a Bandstop FIR filter.

    This class designs a bandstop FIR filter based on the given filter configuration.
    The filter attenuates frequencies within a specified stopband while allowing others to pass.
    The bandstop filter is created by combining two sinc functions, one for the
    lower cutoff frequency and one for the upper cutoff frequency, resulting in
    a filter that rejects frequencies within a specific band.
    """

    def __init__(self, filter_conf: FilterConf, round_to: int = 4):
        """
        Initializes the bandstop filter with the given configuration.

        Args:
            filter_conf (FilterConf): Configuration containing:
                - sampling_freq_hz (float): Sampling frequency in Hz.
                - passband_freq_hz (float): Lower passband frequency in Hz.
                - stopband_freq_hz (float): Lower stopband frequency in Hz.
                - passband_freq2_hz (float): Upper passband frequency in Hz.
                - stopband_freq2_hz (float): Upper stopband frequency in Hz.
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

        self.fp2 = filter_conf.get("passband_freq2_hz", None)
        self.fs2 = filter_conf.get("stopband_freq2_hz", None)

    def _calculate_filter_length(self, d: float) -> int:
        """
        Calculates the filter length (N) based on the transition bandwidth.

        The length of the filter is determined using the sampling frequency and
        the difference between the stopband and passband frequencies.

        Args:
            d (float): The D parameter, used for determining the required filter length.

        Returns:
            int: Computed filter length (N).
        """
        if not d:
            raise ValueError("The design parameter 'd' must be calculated first.")

        N = truncate(
            ((self.F * d) / (min(self.fs - self.fp, self.fp2 - self.fs2))) + 1,
            self.round_to,
        )
        return int(N)

    def calculate_impulse_response_coefficients(self) -> list[float]:
        """
        Computes the impulse response coefficients of the bandstop filter.

        This method calculates the impulse response using the sinc function, ensuring that
        frequencies within the stopband are attenuated, while others are preserved.

        The formula used for calculating the coefficients is:
            c = (1 / (nc * pi)) * (sin(term1) - sin(term2))
        Where:
            term1 = (2 * pi * nc * fc1) / F
            term2 = (2 * pi * nc * fc2) / F
            fc1 = fp + (deltaF / 2) (lower cutoff frequency)
            fc2 = fp2 - (deltaF / 2) (upper cutoff frequency)
            F = sampling frequency
            nc = coefficient index

        Returns:
            list[float]: The list of computed impulse response coefficients.

        Raises:
            ValueError: If the filter order has not been calculated before calling this method.
        """
        if self.n is None:
            raise ValueError("Order must be calculated first. Call calculate_order().")

        nc = 1

        deltaF = min(self.fs - self.fp, self.fp2 - self.fs2)
        fc1 = self.fp + (deltaF / 2)
        fc2 = self.fp2 - (deltaF / 2)

        n0 = (2 / self.F) * (fc1 - fc2) + 1
        self.impulse_response_coefficients.append(n0)

        while nc <= self.n:
            term1 = (2 * math.pi * nc * fc1) / self.F
            term2 = (2 * math.pi * nc * fc2) / self.F
            c = (1 / (nc * math.pi)) * ((math.sin(term1)) - (math.sin(term2)))
            self.impulse_response_coefficients.append(truncate(c, self.round_to))
            nc = nc + 1

        return self.impulse_response_coefficients
