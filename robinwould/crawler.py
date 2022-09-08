"""Module where the decorators are located"""
# pyright: reportGeneralTypeIssues=false

from typing import Any, Callable, Dict, Iterator
from scrapy.selector.unified import Selector
from robinwould import interfaces
from robinwould._utils import ScrapingProcessor, RequestAdapter


class Crawler:
    """Manage the spiders"""

    def __init__(self, proxies: Dict[str, str] = {}):
        self._response_factory = RequestAdapter(proxies)

    def spider(
        self,
        spider_function: Callable[[Selector], Iterator[interfaces.Model]],
        **kwargs: Dict[str, Any]
    ) -> Iterator[Dict[str, Any]]:
        """Decorator for declaring RobinWould spiders

        Args:
            spider_function (Callable[[Selector], Iterator[interfaces.Model]]): the spider
            function

        Yields:
            Iterator[Dict[str, Any]]: the results of the scraping
        """

        url = kwargs.get("url")
        response = self._response_factory.get(url)
        processor = ScrapingProcessor(response)

        scraping_data: interfaces.Model
        for scraping_data in spider_function:
            processed_result = processor.process(scraping_data)

            yield processed_result
