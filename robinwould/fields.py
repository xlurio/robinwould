from typing import Any
from robinwould.exceptions import InvalidFieldValueException
from robinwould.interfaces import Field


class StringField(Field):
    """Field for scraped string data"""

    _field_value: str = ""

    def clean(self) -> Any:
        try:
            return str(self.field_value)

        except ValueError:
            raise InvalidFieldValueException("The passed value is not a valid string")


class IntegerField(Field):
    """Field for scraped integer data"""

    _field_value: Any = 0

    def clean(self) -> Any:
        try:
            return int(self.field_value)

        except ValueError:
            raise InvalidFieldValueException("The passed value is not a valid integer")
