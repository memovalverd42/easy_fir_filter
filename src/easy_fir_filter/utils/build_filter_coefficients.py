"""
This module provides a function to build the symmetric FIR filter coefficients.

The function processes the given FIR filter coefficients to ensure symmetry
and handle small numerical errors, such as negative zero values.
"""


def build_filter_coefficients(fir_coefficients: list[float]) -> list[float]:
    """
    Constructs the symmetric FIR filter coefficients.

    This function processes an input list of FIR filter coefficients to generate
    a symmetric coefficient list. It ensures that values close to zero are correctly
    handled, avoiding negative zero representations.

    Args:
        fir_coefficients (list[float]): The FIR filter coefficients.

    Returns:
        list[float]: A symmetric list of FIR filter coefficients.

    Example:
        >>> build_filter_coefficients([0.2, 0.5, 0.2])
        [0.2, 0.5, 0.2, 0.5]

    Notes:
        - The function ensures that small negative zero values (-0.0) are replaced with 0.
        - The symmetry is achieved by appending a reversed copy of the coefficients,
          excluding the first element to avoid duplication.
    """

    idx = len(fir_coefficients) - 1
    cont = 1
    ordered = []

    # Reverse order and clean zero representations
    while idx >= 0:
        ordered.append(0 if fir_coefficients[idx] == -0.0 else fir_coefficients[idx])
        idx -= 1

    # Append original order (excluding first element) to ensure symmetry
    while cont < len(fir_coefficients):
        ordered.append(0 if fir_coefficients[cont] == -0.0 else fir_coefficients[cont])
        cont += 1

    return ordered
