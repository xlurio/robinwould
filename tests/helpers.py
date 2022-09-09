import os
from typing import Iterator

from scrapy.selector.unified import Selector
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

    with open(example_page_path, "r") as example_page:
        page_content = example_page.read()

    return Selector(text=page_content)


class FakeRequestAdapter(AbstractRequestAdapter):
    async def get(self, url: str) -> Selector:
        return make_example_response()


class FakeModel(Model):
    name = StringField()
    age = IntegerField()


crawler = Crawler()


@crawler.spider(url="https://example.com")  # type: ignore
def fake_spider() -> Iterator[FakeModel]:
    yield FakeModel(
        name='//main/p[@id="name"]/text()',
        age='//main/p[@id="age"]/text()',
    )
