"""
This module defines the IFilter interface for digital filters.
"""

from abc import ABC, abstractmethod


class IFilter(ABC):
    """
    Interface for digital filters.

    This abstract class defines the essential methods that any filter implementation
    must provide, including order calculation and impulse response computation.

    Attributes:
        n (int): The filter order, which is half of the total filter length minus one.
        impulse_response_coefficients (list[float]): The computed impulse response coefficients.
    """

    n: int = None
    impulse_response_coefficients: list[float] = []

    def calculate_filter_order(self, d: float) -> tuple[int, int]:
        """
        Calculates the filter order and length based on the given parameter `d`.

        This method determines the appropriate filter length (N) and order (n) using
        the provided design parameter `d`. The length is adjusted to ensure that it is
        always an odd number, which is a common requirement for symmetrical FIR filters.

        Args:
            d (float): The design parameter used to compute the filter order.

        Returns:
            tuple[int, int]: A tuple containing:
                - n (int): The filter order, defined as (N - 1) / 2.
                - N (int): The total filter length.

        Raises:
            ValueError: If `d` is not provided or has not been calculated.
        """
        if not d:
            raise ValueError(
                "The design parameter 'd' must be calculated first. "
                "Call calculate_d_parameter() before this method."
            )

        filter_length = self._calculate_filter_length(d)

        # Ensure N is odd by adjusting the calculated filter length
        N = filter_length + 2 if (filter_length + 1) % 2 == 0 else filter_length + 1

        self.n = int((N - 1) / 2)  # Compute filter order

        return self.n, N

    @abstractmethod
    def _calculate_filter_length(self, d: float) -> int:
        """
        Computes the initial filter length based on the design parameter `d`.

        This method must be implemented by subclasses to define how the filter
        length is determined from `d`.

        Args:
            d (float): The design parameter for filter length calculation.

        Returns:
            int: The computed filter length (before adjustment to ensure odd length).
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def calculate_impulse_response_coefficients(self) -> list[float]:
        """
        Computes the impulse response coefficients of the filter.

        This method must be implemented by subclasses to generate the specific
        impulse response required for the filter type.

        Returns:
            list[float]: A list containing the computed impulse response coefficients.
        """
        raise NotImplementedError("Subclasses must implement this method.")
