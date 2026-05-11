"""Tests for crawler module."""

from __future__ import annotations

from unittest.mock import MagicMock

import requests

from src.crawler import Crawler


def test_normalize_url_removes_fragment_query_and_trailing_slash() -> None:
    url = "https://quotes.toscrape.com/page/1/?a=1#top"
    normalized = Crawler._normalize_url(url)
    assert normalized == "https://quotes.toscrape.com/page/1"


def test_normalize_url_rejects_non_http_scheme() -> None:
    assert Crawler._normalize_url("mailto:test@example.com") is None


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


def test_crawl_respects_max_pages() -> None:
    crawler = Crawler(base_url="https://quotes.toscrape.com", politeness_seconds=0)

    html_page_1 = """
    <html><body>
      <a href="/page/1/">p1</a>
      <a href="/page/2/">p2</a>
    </body></html>
    """
    html_page_2 = "<html><body><p>page 1</p></body></html>"

    responses = {
        "https://quotes.toscrape.com": html_page_1,
        "https://quotes.toscrape.com/page/1": html_page_2,
        "https://quotes.toscrape.com/page/2": html_page_2,
    }

    crawler._fetch_page = MagicMock(side_effect=lambda url: responses.get(url))

    pages = crawler.crawl(max_pages=2)
    assert len(pages) == 2
    assert pages[0].url == "https://quotes.toscrape.com"


def test_crawl_skips_failed_pages_and_continues() -> None:
    crawler = Crawler(base_url="https://quotes.toscrape.com", politeness_seconds=0)

    html_page_1 = """
    <html><body>
      <a href="/page/1/">p1</a>
      <a href="/page/2/">p2</a>
    </body></html>
    """

    def fake_fetch(url: str) -> str | None:
        if url.endswith("/page/1"):
            return None
        return html_page_1

    crawler._fetch_page = MagicMock(side_effect=fake_fetch)

    pages = crawler.crawl(max_pages=3)
    urls = [p.url for p in pages]

    assert "https://quotes.toscrape.com/page/1" not in urls
    assert "https://quotes.toscrape.com" in urls
