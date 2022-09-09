"""Module reserved for utilities"""

from typing import Any, Callable, Coroutine, Dict
from scrapy.selector.unified import Selector
import aiohttp
from robinwould.exceptions import InvalidResponseException
from robinwould.interfaces import AbstractRequestAdapter, Field, Model


def check_response(response: Any) -> Selector:
    """Check if the passed response is valid for scraping

    Args:
        response (Any): the response to check

    Raises:
        InvalidResponseException: when the response is invalid

    Returns:
        Selector: the validated response
    """

    if isinstance(response, Selector):
        return response

    raise InvalidResponseException("""The passed response is invalid""")


class ScrapingProcessor:
    """Service that process the scraping data received by the spider"""

    def __init__(self, response: Any):
        self._response: Selector = check_response(response)

    def process(self, scraping_data: Model) -> Dict[str, Any]:
        """Scrapes and validates data based on the entered scraped data

        Args:
            scraping_data (Model): the data needed for scrape

        Returns:
            Dict[str, Any]: the scraped data
        """
        data_dict = vars(scraping_data)
        result_data: Dict[str, Any] = {}

        for key in data_dict.keys():
            field: Field = getattr(scraping_data, key)
            scraped_field = self._scrape_field(field)
            validated_value = scraped_field.clean()

            result_data[key] = validated_value

        return result_data

    def _scrape_field(self, field: Field) -> Field:
        xpath = field.xpath
        field_value = self._response.xpath(xpath).get()
        field.field_value = field_value

        return field


class RequestAdapter(AbstractRequestAdapter):
    """Adapts the requests library to create responses that can be consumed by the
    spiders"""

    def __init__(self, proxy: str):
        self._proxy = proxy
        self.request_method = self._get_request_method()

    def _get_request_method(
        self,
    ) -> Callable[
        [str, aiohttp.ClientSession], Coroutine[Any, Any, aiohttp.ClientResponse]
    ]:
        request_method_dict = {
            False: self._request_without_proxy,
            True: self._request_with_proxy,
        }

        have_proxy = len(self._proxy) > 0

        return request_method_dict.get(have_proxy, self._request_without_proxy)

    async def _request_without_proxy(
        self, url: str, session: aiohttp.ClientSession
    ) -> aiohttp.ClientResponse:
        return await session.get(url)

    async def _request_with_proxy(
        self, url: str, session: aiohttp.ClientSession
    ) -> aiohttp.ClientResponse:
        return await session.get(url, proxy=self._proxy)

    async def get(self, url: str, session: aiohttp.ClientSession) -> Selector:
        """Request URL and returns the response to be processed by the spider

        Args:
            url (str): URL to be requested

        Returns:
            Selector: The HTTP response
        """
        received_response = await self.request_method(url, session)
        content = await received_response.text()
        received_response.close()

        return Selector(text=content)
