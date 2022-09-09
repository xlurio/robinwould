"""Module containing utilities for tests"""

import os
from typing import Iterator

from scrapy.selector.unified import Selector
import aiohttp
from robinwould.crawler import Crawler
from robinwould.fields import IntegerField, StringField
from robinwould.interfaces import AbstractRequestAdapter, Model


def get_example_page_path() -> str:
    """Returns the path to the example page for tests

    Returns:
        str: the path to the example page HTML file
    """
    package = os.path.dirname(__file__)
    package_dir = os.path.abspath(package)
    resources_dir = os.path.join(package_dir, "resources/example.html")

    return resources_dir


def make_example_response() -> Selector:
    """Returns a fake HTTP response for tests

    Returns:
        Selector: the response to process
    """
    example_page_path = get_example_page_path()
    page_content: str = ""

    with open(example_page_path, "r", encoding="utf8") as example_page:
        page_content = example_page.read()

    return Selector(text=page_content)


class FakeRequestAdapter(AbstractRequestAdapter):
    """Request adapter for tests"""

    async def get(self, url: str, session: aiohttp.ClientSession) -> Selector:
        return make_example_response()


class FakeModel(Model):
    """Scraping data model for tests"""

    name = StringField()
    age = IntegerField()


crawler = Crawler()


@crawler.spider(url="https://example.com")  # type: ignore
def fake_spider(response: Selector) -> Iterator[FakeModel]:
    """Spider for tests

    Yields:
        Iterator[FakeModel]: the scraping data
    """
    yield FakeModel(
        name='//main/p[@id="name"]/text()',
        age='//main/p[@id="age"]/text()',
    )
