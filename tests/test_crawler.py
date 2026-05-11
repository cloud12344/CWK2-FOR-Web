"""Tests for crawler module."""

from __future__ import annotations

from unittest.mock import MagicMock

import requests

from src.crawler import Crawler


def test_normalize_url_removes_fragment_query_and_trailing_slash() -> None:
    url = "https://quotes.toscrape.com/page/1/?a=1#top"
    normalized = Crawler._normalize_url(url)
    assert normalized == "https://quotes.toscrape.com/page/1"


def test_extract_links_keeps_only_same_domain() -> None:
    crawler = Crawler(base_url="https://quotes.toscrape.com/")
    html = """
    <html><body>
      <a href="/page/1/">Page1</a>
      <a href="https://example.com/page/2/">External</a>
      <a href="#fragment">Fragment</a>
    </body></html>
    """

    links = crawler._extract_links("https://quotes.toscrape.com/", html)
    assert "https://quotes.toscrape.com/page/1" in links
    assert all("example.com" not in link for link in links)


def test_fetch_page_handles_request_exception_and_returns_none() -> None:
    crawler = Crawler(base_url="https://quotes.toscrape.com/", politeness_seconds=0)

    mocked_get = MagicMock(side_effect=requests.RequestException("network error"))
    crawler.session.get = mocked_get

    result = crawler._fetch_page("https://quotes.toscrape.com/")
    assert result is None
