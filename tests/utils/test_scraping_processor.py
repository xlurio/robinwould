"""Module containing the tests for the scraping data processor"""

from typing import Any, Callable, Dict
import pytest
from robinwould.exceptions import InvalidFieldValueException
from robinwould.interfaces import Model
from robinwould._utils import ScrapingProcessor
from tests.helpers import FakeModel, make_example_response


class TestScrapingProcessor:
    """Tests for the scraping data processor"""

    @pytest.fixture
    def _valid_data(self) -> Model:
        return FakeModel(
            name='//main/p[@id="name"]/text()',
            age='//main/p[@id="age"]/text()',
        )

    def test_process_valid_data(self, _valid_data: Model) -> None:
        """When valid scraping data is passed, it should be successfully scraped"""
        result = self._when_processed(_valid_data)
        self._then_should_return_result_dictionary(result)

    def _then_should_return_result_dictionary(self, result: Dict[str, Any]) -> None:
        expected_result = {"name": "Carlos", "age": 32}

        assert result == expected_result

    @pytest.fixture
    def _invalid_data(self) -> Model:
        return FakeModel(
            name='//main/p[@id="name"]/text()',
            age='//main/p[@id="occupation"]/text()',
        )

    def test_process_invalid_data(self, _invalid_data: Model) -> None:
        """When invalid scraping data is passed, it should raise and exception"""

        def result() -> None:
            self._when_processed(_invalid_data)

        self._then_should_raise_exception(result)

    def _when_processed(self, scraping_data: Model) -> Dict[str, Any]:
        response = make_example_response()
        processor = ScrapingProcessor(response)

        return processor.process(scraping_data)

    def _then_should_raise_exception(self, result: Callable[[], None]) -> None:
        with pytest.raises(InvalidFieldValueException):
            result()
