"""
This module defines the IWindow interface for window functions used in digital filter design.
"""

from abc import ABC, abstractmethod
from typing import overload


class IWindow(ABC):
    """
    Interface for window functions in digital signal processing.

    This abstract class defines the required method for computing the coefficients
    of a window function, which is typically used to shape the impulse response
    of a finite impulse response (FIR) filter. Window functions are essential for
    controlling the trade-off between main lobe width and side lobe level in the
    frequency response of the filter, thereby reducing spectral leakage.

    Attributes:
        window_coefficients (list[float]): The window coefficients.
    """

    window_coefficients: list[float] = []

    @overload
    @abstractmethod
    def calculate_window_coefficients(
        self, n: int, filter_length: int
    ) -> list[float]: ...

    @overload
    @abstractmethod
    def calculate_window_coefficients(
        self, n: int, filter_length: int, AS: float
    ) -> list[float]: ...

    @abstractmethod
    def calculate_window_coefficients(
        self, n: int, filter_length: int, AS: float | None = None
    ) -> list[float]:
        """
        Computes the window function coefficients for a given filter order.

        Window functions are applied to FIR filter designs to control spectral leakage
        and shape the frequency response. Different window types (e.g., Hamming, Kaiser,
        Blackman) modify the trade-off between main lobe width and side lobe level.

        Args:
            n (int): The filter order (number of coefficients - 1).
            filter_length (int): The total length of the FIR filter.
            AS (float, optional): Additional shape parameter for specific window functions,
                such as the Kaiser window, where AS represents the stopband attenuation.
                If provided, it allows for more precise control over the window's shape.

        Returns:
            list[float]: A list containing the computed window function coefficients.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Notes:
            The method can be overloaded:
                - When 'AS' is not provided, the window coefficients are calculated
                  using only the filter order and length. This is typically used for
                  fixed-shape windows like Hamming or Hanning.
                - When 'AS' is provided, the window coefficients are calculated
                  with an additional shape parameter, allowing for more flexible
                  window design, as in the Kaiser window.
        """
        raise NotImplementedError("Subclasses must implement this method.")
