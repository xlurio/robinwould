"""Module containing all the tests against the request adapter"""

from robinwould._utils import RequestAdapter


class TestRequestAdapter:
    """Tests for the request adapter"""

    def test_getting_with_proxy_request(self) -> None:
        """When adapter is created with a proxy, it should request with it"""
        result = self._when_adapter_is_created("proxy")
        self._then_should_use_with_proxy_request(result)

    def _then_should_use_with_proxy_request(self, result: str) -> None:
        expected_result = "_request_with_proxy"

        assert result == expected_result

    def test_getting_without_proxy_request(self) -> None:
        """When adapter is created without a proxy, it should request without it"""
        result = self._when_adapter_is_created("")
        self._then_should_use_without_proxy_request(result)

    def _when_adapter_is_created(self, proxy: str) -> str:
        adapter = RequestAdapter(proxy)
        request_method = adapter.request_method

        return request_method.__name__

    def _then_should_use_without_proxy_request(self, result: str) -> None:
        expected_result = "_request_without_proxy"

        assert result == expected_result
