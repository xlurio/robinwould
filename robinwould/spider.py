"""Module that contains the Spider models"""

from typing import Callable, Iterator
from scrapy.selector.unified import Selector
from robinwould import interfaces


class Spider:
    """Stores the information for scraping"""

    _url: str

    def __init__(
        self,
        spider_function: Callable[[Selector], Iterator[interfaces.Model]],
        url: str,
    ):
        self._spider_function = spider_function
        self._url = url

    @property
    def spider_function(self) -> Callable[[Selector], Iterator[interfaces.Model]]:
        """Stores the callable spider"""
        return self._spider_function

    @property
    def url(self) -> str:
        """Stores the initial URL to scrape"""
        return self._url
