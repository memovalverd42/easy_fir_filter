"""
This file contains the implementation of the Kaiser window class.
"""

import math

from easy_fir_filter.interfaces.window_interface import IWindow
from easy_fir_filter.utils import truncate


class KaiserWindow(IWindow):
    """
    Implementation of the Kaiser Window.

    The Kaiser window is commonly used in digital signal processing
    to design FIR filters with a specified stopband attenuation. It
    offers flexibility in controlling the trade-off between main lobe
    width and side lobe attenuation, making it suitable for applications
    where precise control over filter characteristics is required.
    """

    def __init__(self, round_to: int = 4):
        """
        Initializes the Kaiser window.

        Args:
            round_to (int, optional): Number of decimal places to round
                                      the window coefficients. Defaults to 4.
        """
        self.window_coefficients = []
        self.round_to = round_to

        self.alpha: float | None = None
        self.betas = []

    def _calculate_alpha_parameter(self, AS: float) -> float:
        """
        Calculates the alpha parameter based on the stopband attenuation (AS).

        The alpha parameter determines the shape of the Kaiser window.

        Args:
            AS (float): The stopband attenuation in dB.

        Returns:
            float: The calculated alpha parameter.
        """
        if AS is None:
            raise ValueError("Stopband attenuation (AS) must be provided")

        if AS <= 21:
            self.alpha = 0.0
        elif 21 < AS <= 50:
            self.alpha = truncate(
                (0.5842 * (AS - 21) ** 0.4) + 0.07886 * (AS - 21), self.round_to
            )
        else:
            self.alpha = truncate(0.1102 * (AS - 8.7), self.round_to)

        return self.alpha

    def _calculate_betas(self, n: int, filter_length: int) -> list[float]:
        """
        Calculates the beta values for each coefficient index.

        The beta values are used in the calculation of the Kaiser window coefficients.

        Args:
            n (int): The filter order.
            filter_length (int): The total length of the filter (N).

        Returns:
            list[float]: List of beta values.
        """
        if self.alpha is None:
            raise ValueError("Alpha parameter must be calculated first")

        nc = 0
        while nc <= n:
            b = self.alpha * (1 - ((2 * nc) / (filter_length - 1)) ** 2) ** 0.5
            self.betas.append(truncate(b, self.round_to))
            nc = nc + 1

        return self.betas

    def _calculate_i_alpha(self, alpha: float) -> float:
        """
        Calculates the modified Bessel function of the first kind, I0(alpha).

        This function is used in the calculation of the Kaiser window coefficients.

        Args:
            alpha (float): The alpha parameter.

        Returns:
            float: The calculated I0(alpha) value.
        """
        if alpha is None:
            raise ValueError("Alpha parameter must be provided")

        if alpha == 0:
            return 1

        k = 1
        result = 0
        while k <= 25:
            result += truncate(
                ((1 / math.factorial(k)) * (alpha / 2) ** k) ** 2, self.round_to
            )
            k = k + 1

        return result + 1

    def calculate_window_coefficients(
        self, n: int, filter_length: int, AS: float = None
    ) -> list[float]:
        """
        Computes the Kaiser window coefficients.

        The Kaiser window coefficients are calculated using the alpha parameter,
        beta values, and the modified Bessel function of the first kind.

        Args:
            n (int): The filter order.
            filter_length (int): The total length of the filter (N).
            AS (float, optional): The stopband attenuation in dB. Defaults to None.

        Returns:
            list[float]: List of Kaiser window coefficients.
        """
        if n is None or filter_length is None:
            raise ValueError("Filter order (n) and filter length (N) must be provided")

        if AS is None:
            raise ValueError("Stopband attenuation (AS) not provided")

        # Calculate alpha
        self._calculate_alpha_parameter(AS=AS)

        # Calculate betas
        self._calculate_betas(n=n, filter_length=filter_length)

        i_alpha = self._calculate_i_alpha(self.alpha)
        for beta in self.betas:

            self.window_coefficients.append(
                truncate(self._calculate_i_alpha(beta) / i_alpha, self.round_to)
            )

        return self.window_coefficients
