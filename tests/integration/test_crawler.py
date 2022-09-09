"""Module containing all the tests against the crawler"""

from typing import Any, Dict, List
import pytest
from tests.helpers import crawler, FakeRequestAdapter

pytestmark = pytest.mark.anyio


class TestCrawler:
    """Tests for the crawler"""

    def test_running(self):
        """When the crawler is runned, it should scrape data"""
        result = self._when_runned()
        self._then_should_scrape_data(result)

    def _when_runned(self) -> List[Dict[str, Any]]:
        crawler.response_factory = FakeRequestAdapter()
        return crawler.run()

    def _then_should_scrape_data(self, result: List[Dict[str, Any]]) -> None:
        expected_result = [{"name": "Carlos", "age": 32}]

        assert result == expected_result
