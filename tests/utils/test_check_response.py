"""Module containing all the tests against the response validating functions"""

from typing import Any, Callable
import pytest
from scrapy.selector.unified import Selector
from robinwould._utils import check_response
from robinwould.exceptions import InvalidResponseException
from tests.helpers import make_example_response


class TestCheckResponse:
    """Test check_response function"""

    @pytest.fixture
    def _valid_response(self) -> Selector:
        return make_example_response()

    def test_valid_response(self, _valid_response: Selector) -> None:
        """When a valid response is passed as parameter, then it should return it"""
        result = self._when_validated(_valid_response)
        self._then_should_return_it(result)

    def _then_should_return_it(self, result: Selector) -> None:
        assert isinstance(result, Selector) is True

    def test_invalid_response(self) -> None:
        """When a valid response is passed as parameter, then it should return it"""

        def result() -> None:
            self._when_validated("invalid_response")

        self._then_should_raise_exception(result)

    def _then_should_raise_exception(self, result: Callable[[], None]) -> None:
        with pytest.raises(InvalidResponseException):
            result()

    def _when_validated(self, response: Any) -> Selector:
        return check_response(response)
