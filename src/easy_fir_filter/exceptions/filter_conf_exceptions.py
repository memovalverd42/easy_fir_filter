"""
This file contains the definitions of the exceptions used in the filter_conf module.
"""


class FilterConfValidationError(Exception):
    """Base class for all filter configuration validation errors."""


class MissingKeysError(FilterConfValidationError):
    """Raised when a filter configuration is missing required keys."""

    def __init__(self, missing_keys: list[str]):
        super().__init__(f"Missing required keys: {', '.join(missing_keys)}")
        self.missing_keys = missing_keys


class InvalidTypeError(FilterConfValidationError):
    """Raised when a filter configuration has an invalid type for a key."""

    def __init__(self, key: str, expected_type: type, actual_type: type):
        super().__init__(
            f"Invalid type for key '{key}'. Expected {expected_type}, got {actual_type}."
        )
        self.key = key
        self.expected_type = expected_type
        self.actual_type = actual_type
