"""Web crawler for quotes.toscrape.com with politeness delay."""

from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


@dataclass
class PageResult:
    """Single crawled page result."""

    url: str
    html: str


class Crawler:
    """Crawl pages from a single domain with a fixed politeness delay."""

    def __init__(
        self,
        base_url: str,
        politeness_seconds: float = 6.0,
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        parsed = urlparse(self.base_url)
        self.allowed_domain = parsed.netloc
        self.politeness_seconds = politeness_seconds
        self.timeout = timeout
        self.session = requests.Session()

    def crawl(self, max_pages: Optional[int] = None) -> List[PageResult]:
        """Breadth-first crawl starting from base_url."""
        queue: List[str] = [self.base_url]
        visited: Set[str] = set()
        results: List[PageResult] = []

        while queue:
            if max_pages is not None and len(results) >= max_pages:
                break

            current_url = queue.pop(0)
            if current_url in visited:
                continue
            visited.add(current_url)

            html = self._fetch_page(current_url)
            if html is None:
                continue

            results.append(PageResult(url=current_url, html=html))

            for link in self._extract_links(current_url, html):
                if link not in visited and link not in queue:
                    queue.append(link)

        return results

    def _fetch_page(self, url: str) -> Optional[str]:
        """Fetch a single page and respect politeness window."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None
        finally:
            sleep(self.politeness_seconds)

    def _extract_links(self, current_url: str, html: str) -> List[str]:
        """Extract valid in-domain links from page HTML."""
        soup = BeautifulSoup(html, "html.parser")
        links: List[str] = []

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"].strip()
            if not href:
                continue

            absolute_url = urljoin(current_url, href)
            cleaned_url = self._normalize_url(absolute_url)
            if cleaned_url and self._is_allowed_url(cleaned_url):
                links.append(cleaned_url)

        return links

    @staticmethod
    def _normalize_url(url: str) -> Optional[str]:
        """Normalize URL by removing fragments and trailing slash."""
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return None

        path = parsed.path.rstrip("/")
        if path == "":
            path = "/"

        normalized = parsed._replace(fragment="", query="", path=path)
        return normalized.geturl()

    def _is_allowed_url(self, url: str) -> bool:
        """Allow only same-domain pages."""
        parsed = urlparse(url)
        return parsed.netloc == self.allowed_domain


def crawl_site(base_url: str, max_pages: Optional[int] = None) -> List[Dict[str, str]]:
    """Convenience function used by CLI."""
    crawler = Crawler(base_url=base_url)
    pages = crawler.crawl(max_pages=max_pages)
    return [{"url": page.url, "html": page.html} for page in pages]
