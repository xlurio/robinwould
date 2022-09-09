"""Module where the decorators are located"""
# pyright: reportGeneralTypeIssues=false

import asyncio
from typing import Any, Callable, Dict, Iterator, List
import logging
from aiohttp.client_exceptions import ClientConnectionError
import aiohttp
from scrapy.selector.unified import Selector
from robinwould import interfaces
from robinwould._utils import ScrapingProcessor, RequestAdapter
from robinwould.spider import Spider


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

        logging.basicConfig()
        self._logger = logging.getLogger(__name__)

    def run(self) -> List[Dict[str, Any]]:
        """Run all the spiders attached to the crawler object and returns the scraped
        data

        Returns:
            List[Dict[str, Any]]: the scraped data
        """
        return asyncio.run(self._run_all())

    async def _run_all(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            future_results = [
                asyncio.create_task(self._get_results(spider, session))
                for spider in self.spiders
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

    async def _get_results(self, spider: Spider, session: aiohttp.ClientSession):
        received_results: List[interfaces.Model] = []
        result: Dict[str, Any]
        i = 0

        async for result in self._run_spider(spider, session):
            received_results.append(result)
            i += 1

            if i == 3:
                return received_results

        return received_results

    async def _run_spider(
        self, spider: Spider, session: aiohttp.ClientSession
    ) -> Iterator[Dict[str, Any]]:
        self._logger.debug("Requesting %s", spider.url)

        try:
            response = await self.response_factory.get(spider.url, session)
            self._logger.debug("Response from %s received", spider.url)

        except ClientConnectionError as error:
            self._logger.error(
                "%s: Not able to connect to %s",
                error,
                spider.url,
            )
            return

        processor = ScrapingProcessor(response)

        scraping_data: interfaces.Model

        for scraping_data in spider.spider_function(response):
            processed_result = processor.process(scraping_data)

            self._logger.debug("Data scraped: %s", processed_result)
            print(f"Data scraped: {processed_result}")
            yield processed_result

        await asyncio.sleep(self._download_delay)

    def spider(
        self,
        url: str,
    ) -> Callable[[Callable[[Selector], Iterator[interfaces.Model]]], None]:
        """Decorator to declare spiders

        Args:
            url (str): the URL to be scraped by the spider

        Returns:
            Callable[[Callable[[Selector], Iterator[interfaces.Model]]], None]: the
            function for attaching spiders to the crawler object
        """

        def add_spider(
            spider_function: Callable[[Selector], Iterator[interfaces.Model]]
        ) -> None:
            """Attach spiders to the crawler object

            Args:
                spider_function (Callable[[Selector], Iterator[interfaces.Model]]): the
                wrapped spider
            """
            new_spider = Spider(spider_function, url)
            self.spiders.append(new_spider)

        return add_spider
