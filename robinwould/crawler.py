"""Module where the decorators are located"""
# pyright: reportGeneralTypeIssues=false

import asyncio
from typing import Any, Callable, Dict, Iterable, Iterator, List
from scrapy.selector.unified import Selector
from robinwould import interfaces
from robinwould._utils import ScrapingProcessor, RequestAdapter
from robinwould.spider import Spider
import logging


class Crawler:
    """Manage the spiders"""

    spiders: List[Spider] = []

    def __init__(
        self,
        download_delay: int = 5,
        proxy: str = "",
        pipelines: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = [],
    ) -> None:
        self._download_delay = download_delay
        self._response_factory = RequestAdapter(proxy)
        self._pipelines = pipelines
        self._logger = logging.getLogger(__name__)

    async def run(self) -> Iterable[Dict[str, Any]]:
        future_results = [self._get_results(spider) for spider in self.spiders]

        return await asyncio.gather(future_results)  # type: ignore

    async def _get_results(self, spider: Spider):
        results: List[interfaces.Model] = []

        while True:
            try:
                result: Dict[str, Any] = self._run_spider(spider).__anext__()  # type: ignore
                results.append(result)

            except StopAsyncIteration:
                return results

    async def _run_spider(self, spider: Spider) -> Iterator[Dict[str, Any]]:
        self._logger.debug(f"Requesting {spider.url}")
        response = await self._response_factory.get(spider.url)
        self._logger.debug(f"Response from {spider.url} received")

        processor = ScrapingProcessor(response)

        scraping_data: interfaces.Model
        for scraping_data in spider.spider_function():
            processed_result = processor.process(scraping_data)

            self._logger.debug(f"Data scraped: {processed_result}")
            yield processed_result

        await asyncio.sleep(self._download_delay)

    def spider(
        self,
        url: str,
    ) -> None:
        """Decorator for declaring RobinWould spiders

        Args:
            spider_function (Callable[[Selector], Iterator[interfaces.Model]]): the spider
            function
            url [str]: the initial URL to scrape
        """

        def add_spider(
            spider_function: Callable[[Selector], Iterator[interfaces.Model]]
        ):
            new_spider = Spider(spider_function, url)
            self.spiders.append(new_spider)

        return add_spider
