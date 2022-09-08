"""Module where the decorators are located"""
# pyright: reportGeneralTypeIssues=false

from typing import Any, Callable, Dict, Iterator, List
from scrapy.selector.unified import Selector
from robinwould import interfaces
from robinwould._utils import ScrapingProcessor, RequestAdapter
from robinwould.spider import Spider


class Crawler:
    """Manage the spiders"""

    spiders: List[Spider] = []

    def __init__(
        self,
        proxies: Dict[str, str] = {},
        pipelines: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = [],
    ) -> None:
        self._response_factory = RequestAdapter(proxies)
        self._pipelines = pipelines

    def spider(
        self,
        spider_function: Callable[[Selector], Iterator[interfaces.Model]],
        url: str,
    ) -> Iterator[Dict[str, Any]]:
        """Decorator for declaring RobinWould spiders

        Args:
            spider_function (Callable[[Selector], Iterator[interfaces.Model]]): the spider
            function

        Yields:
            Iterator[Dict[str, Any]]: the results of the scraping
        """

        new_spider = Spider(spider_function, url)
        self.spiders.append(new_spider)

    def run(self) -> None:
        pass

    def _run_spider(self, spider: Spider) -> Iterator[Dict[str, Any]]:
        response = self._response_factory.get(spider.url)
        processor = ScrapingProcessor(response)

        scraping_data: interfaces.Model
        for scraping_data in spider.spider_function():
            processed_result = processor.process(scraping_data)

            yield processed_result
