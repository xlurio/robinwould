"""Module where the interfaces are located"""
import abc
from typing import Any, Dict
from scrapy.selector.unified import Selector
import aiohttp


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

    @xpath.setter
    def xpath(self, value: str) -> None:
        self._xpath = value

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


class Model(abc.ABC):
    """Interface for the RobinWould models that should be yield by the spiders"""

    def __init__(self, **kwargs: str):
        xpath: Any
        self.__dict__: Dict[str, Field] = {}

        for key, xpath in kwargs.items():
            field: Field = getattr(self, key)
            field.xpath = xpath

            self.__dict__[key] = field


class AbstractRequestAdapter(abc.ABC):
    """Interface for sending HTTP requests"""

    @abc.abstractmethod
    async def get(self, url: str, session: aiohttp.ClientSession) -> Selector:
        """Sends a request to the passed URL and returns the response to be consumed
        by the spider"""
        raise NotImplementedError()
