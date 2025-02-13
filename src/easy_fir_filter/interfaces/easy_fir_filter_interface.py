"""
This module defines the abstract base class for the EasyFirFilter package.
"""

from abc import ABC, abstractmethod


class IEasyFirFilter(ABC):
    """
    Abstract base class for designing FIR (Finite Impulse Response) filters.

    This interface defines the essential methods required for computing various
    parameters and coefficients necessary for FIR filter design. Any concrete
    implementation must provide specific logic for these calculations.

    Methods:
        - calculate_filter(): Computes the FIR filter coefficients.
        - calculate_delta(): Determines the unified tolerance (delta) for passband and stopband.
        - calculate_ripples(): Computes the passband ripple and stopband attenuation.
        - calculate_d_parameter(): Calculates the D parameter used in filter design.
        - calculate_filter_order(): Determines the filter order.
        - _calculate_filter_coefficients(): Computes the final filter coefficients.
    """

    @abstractmethod
    def calculate_filter(self) -> list[float]:
        """
        Computes the FIR filter coefficients step by step.

        Returns:
            list[float]: A list of computed FIR filter coefficients.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_delta(self) -> float:
        """
        Determines the delta value, which represents the unified tolerance
        for both the passband and stopband.

        Returns:
            float: The computed delta value.
        Raises:
            ValueError: If the delta value is not calculated
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_ripples(self) -> tuple[float, float]:
        """
        Computes the ripple values for the filter.

        The method calculates:
            - A's: Minimum stopband attenuation (in dB).
            - A'p: Maximum allowed ripple in the passband (in dB).

        Returns:
            tuple[float, float]: A tuple containing (A's, A'p), where:
                - A's (float): Minimum stopband attenuation in dB.
                - A'p (float): Maximum passband ripple in dB.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_d_parameter(self) -> float:
        """
        Computes the D parameter, which is used in FIR filter design calculations.

        Returns:
            float: The computed D parameter.
        """
        raise NotImplementedError

    @abstractmethod
    def _calculate_filter_coefficients(self) -> list[float]:
        """
        Computes the final FIR filter coefficients.

        The coefficients are typically obtained as a product of the window function
        A(n) and the ideal impulse response H(n).

        Returns:
            list[float]: A list of computed FIR filter coefficients.
        """
        raise NotImplementedError
