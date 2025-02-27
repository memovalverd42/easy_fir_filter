"""
This file contains the implementation of the Blackman window class.
"""

import math

from easy_fir_filter.interfaces.window_interface import IWindow
from easy_fir_filter.utils import truncate


class BlackmanWindow(IWindow):
    """
    Implementation of the Blackman Window.

    The Blackman window is commonly used in digital signal processing
    to reduce spectral leakage when designing FIR filters.
    """

    def __init__(self, round_to: int = 4):
        """
        Initializes the Blackman window.

        Args:
            round_to (int, optional): Number of decimal places to round
                                      the window coefficients. Defaults to 4.
        """
        self.round_to = round_to

    def calculate_window_coefficients(
        self, n: int, filter_length: int, AS: float | None = None
    ) -> list[float]:
        """
        Computes the Blackman window coefficients.

        Args:
            n (int): The filter order.
            filter_length (int): The total length of the filter (N).
            AS (float, optional): Additional shape parameter for specific window functions

        Returns:
            list[float]: List of Hamming window coefficients.
        """

        self.window_coefficients = [
            truncate(
                0.42
                + 0.5 * math.cos((2 * math.pi * i) / (filter_length - 1))
                + 0.08 * math.cos((4 * math.pi * i) / (filter_length - 1)),
                self.round_to,
            )
            for i in range(n + 1)
        ]

        return self.window_coefficients
