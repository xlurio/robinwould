from tests.helpers import crawler


class TestCrawler:
    """Tests for the crawler"""

    async def test_running(self):
        await crawler.run()

        assert 0 == 2
