"""Module where the decorators are located"""
# pyright: reportGeneralTypeIssues=false

from typing import Any, Callable, Dict, Iterator
from scrapy.selector.unified import Selector
from robinwould import interfaces
from robinwould.utils import ScrapingProcessor, check_response


def spider(
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

    response = kwargs.get("response", None)
    processor = ScrapingProcessor(response)

    result: interfaces.Model
    for result in spider_function:
        processed_result = processor.process(result)

        yield processed_result
