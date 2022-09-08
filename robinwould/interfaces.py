"""Module where the interfaces are located"""
import abc
from typing import Any


class Model(abc.ABC):
    """Interface for the RobinWould models that should be yield by the spiders"""


class Field(abc.ABC):
    """Interface for the RobinWould fields to define the models"""

    _xpath: str
    _field_value: Any = None

    @property
    def xpath(self) -> str:
        """Property that stores the XPath selector for reaching the field desired value

        Returns:
            str: the XPath selector
        """
        return self._xpath

    @property
    def field_value(self) -> Any:
        """Property that stores the scraped value

        Returns:
            Any: the scraped value
        """
        return self._value

    @field_value.setter
    def field_value(self, value: Any) -> None:
        self._value = value

    @abc.abstractmethod
    def clean(self) -> Any:
        """Validates the scraped value

        Raises:
            NotImplementedError: when the method is not implemented
            InvalidFieldValueException: when the value is invalid

        Returns:
            Any: the scraped value
        """
        raise NotImplementedError()
