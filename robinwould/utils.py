"""Module reserved for utilities"""

from typing import Any, Dict
from scrapy.selector.unified import Selector
from robinwould.exceptions import InvalidResponseException
from robinwould.interfaces import Field, Model


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
            field = getattr(scraping_data, key)
            scraped_field = self._scrape_field(field)
            validated_value = self._validate_field_value(scraped_field)

            result_data[key] = validated_value

        return result_data

    def _scrape_field(self, field: Field) -> Field:
        xpath = field.xpath
        field_value = self._response.xpath(xpath).get()
        field.field_value = field_value

        return field

    def _validate_field_value(self, field: Field):
        return field.clean()
