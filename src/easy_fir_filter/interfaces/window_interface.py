"""
This module defines the IWindow interface for window functions used in digital filter design.
"""

from typing import overload
from abc import ABC, abstractmethod


class IWindow(ABC):
    """
    Interface for window functions in digital signal processing.

    This abstract class defines the required method for computing the coefficients
    of a window function, which is typically used to shape the impulse response
    of a finite impulse response (FIR) filter.

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

        Window functions are applied to FIR filter designs to control spectral leakage.
        Different window types (e.g., Hamming, Kaiser, Blackman) modify the shape
        of the filter's frequency response.

        Args:
            n (int): The filter order (number of coefficients - 1).
            filter_length (int): The total length of the FIR filter.
            AS (float, optional): Additional shape parameter for specific window functions.

        Returns:
            list[float]: A list containing the computed window function coefficients.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")
