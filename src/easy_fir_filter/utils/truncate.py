"""
This module provides a function to truncate a floating-point number to a specified number of decimal places.
"""

import math


def truncate(number: float, decimals: int) -> float:
    """
    Truncates a floating-point number to the specified number of decimal places.

    This function removes the digits beyond the given decimal point without rounding.

    Args:
        number (float): The floating-point number to truncate.
        decimals (int): The number of decimal places to retain.

    Returns:
        float: The truncated floating-point number.

    Raises:
        ValueError: If the number of decimals is negative.

    Example:
        >>> truncate(3.14159, 2)
        3.14
        >>> truncate(123.45678, 0)
        123.0
    """
    if decimals < 0:
        raise ValueError("The number of decimals must be non-negative")
    factor = 10.0**decimals
    return math.trunc(number * factor) / factor
