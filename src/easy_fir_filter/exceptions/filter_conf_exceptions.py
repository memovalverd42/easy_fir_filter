"""
This module defines custom exceptions for validating filter configurations.

These exceptions are specifically designed to handle errors related to the
structure and content of filter configuration dictionaries, ensuring that
the configurations meet the required specifications for filter design.
"""


class FilterConfValidationError(Exception):
    """
    Base class for all filter configuration validation errors.

    This class serves as a parent for specific validation errors related to
    filter configurations. It provides a common base for catching and handling
    errors during the validation process.
    """

    pass  # No additional methods or attributes needed for the base class.


class MissingKeysError(FilterConfValidationError):
    """
    Raised when a filter configuration is missing required keys.

    This exception is raised when a dictionary representing a filter configuration
    lacks one or more keys that are mandatory for the filter design process.

    Attributes:
        missing_keys (list[str]): A list of strings representing the missing keys.
    """

    def __init__(self, missing_keys: list[str]):
        """
        Initializes the MissingKeysError with a list of missing keys.

        Args:
            missing_keys (list[str]): A list of strings representing the missing keys.
        """
        super().__init__(f"Missing required keys: {', '.join(missing_keys)}")
        self.missing_keys = missing_keys


class InvalidTypeError(FilterConfValidationError):
    """
    Raised when a filter configuration has an invalid type for a key.

    This exception is raised when the value associated with a key in a filter
    configuration dictionary has an unexpected data type.

    Attributes:
        key (str): The key with the invalid type.
        expected_type (type): The expected data type for the key.
        actual_type (type): The actual data type found for the key.
    """

    def __init__(self, key: str, expected_type: type, actual_type: type):
        """
        Initializes the InvalidTypeError with the key, expected type, and actual type.

        Args:
            key (str): The key with the invalid type.
            expected_type (type): The expected data type for the key.
            actual_type (type): The actual data type found for the key.
        """
        super().__init__(
            f"Invalid type for key '{key}'. Expected {expected_type}, got {actual_type}."
        )
        self.key = key
        self.expected_type = expected_type
        self.actual_type = actual_type
