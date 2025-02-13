"""
This module contains a function to truncate a float number to a given number of decimals.
"""

import math


def truncate(number: float, decimals: int) -> float:
    """
    Truncate a float number to a given number of decimals.
    :param number: Number to truncate
    :param decimals: Number of decimals
    :return: Number truncated
    """
    if decimals < 0:
        raise ValueError("The number of decimals must be non-negative")
    factor = 10.0**decimals
    return math.trunc(number * factor) / factor
