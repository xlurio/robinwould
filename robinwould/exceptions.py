"""Module containing all exceptions of the package"""


class InvalidResponseException(Exception):
    """Raised when a invalid response is passed"""


class InvalidFieldValueException(Exception):
    """Raised when the field value does not passes on validation"""
