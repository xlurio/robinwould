"""Module where the decorators are located"""
# pyright: reportGeneralTypeIssues=false

import asyncio
from typing import Any, Callable, Dict, Iterator, List
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
        self.response_factory: interfaces.AbstractRequestAdapter = RequestAdapter(proxy)
        self._pipelines = pipelines
        self._logger = logging.getLogger(__name__)

    async def run(self) -> List[Dict[str, Any]]:
        future_results = [
            asyncio.create_task(self._get_results(spider)) for spider in self.spiders
        ]
        received_results = await asyncio.gather(*future_results)

        return self._extract_results(received_results)

    def _extract_results(
        self, received_results: List[List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        extracted: List[Dict[str, Any]] = []

        for inner_results in received_results:
            self._extract_inner_results(extracted, inner_results)

        return extracted

    def _extract_inner_results(
        self,
        inner_results_list: List[Dict[str, Any]],
        received_results: List[Dict[str, Any]],
    ) -> None:

        for inner_result in received_results:
            inner_results_list.append(inner_result)

    async def _get_results(self, spider: Spider):
        received_results: List[interfaces.Model] = []
        result: Dict[str, Any]
        i = 0

        async for result in self._run_spider(spider):
            received_results.append(result)
            i += 1

            if i == 3:
                return received_results

        return received_results

    async def _run_spider(self, spider: Spider) -> List[Dict[str, Any]]:
        self._logger.debug("Requesting %s", spider.url)
        response = await self.response_factory.get(spider.url)
        self._logger.debug("Response from %s received", spider.url)

        processor = ScrapingProcessor(response)

        scraping_data: interfaces.Model

        for scraping_data in spider.spider_function():
            processed_result = processor.process(scraping_data)

            self._logger.debug("Data scraped: %s", processed_result)
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
