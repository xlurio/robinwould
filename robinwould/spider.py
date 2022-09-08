from typing import Callable, Iterator
from scrapy.selector.unified import Selector
from robinwould import interfaces


class Spider:
    _spider_function: Callable[[Selector], Iterator[interfaces.Model]]
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
        return self._spider_function

    @property
    def url(self) -> str:
        return self._url
