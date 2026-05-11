"""Index building logic for the coursework search tool."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Tuple

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9']+")


def tokenize(text: str) -> List[str]:
    """Split text into lowercase tokens."""
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


def _extract_page_text(html: str) -> str:
    """Extract quote text and author text from html page.

    For this coursework target website, quote + author text is sufficient and
    keeps index noise low.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    chunks: List[str] = []

    for quote_block in soup.select("div.quote"):
        quote_text = quote_block.select_one("span.text")
        author_text = quote_block.select_one("small.author")

        if quote_text and quote_text.get_text(strip=True):
            chunks.append(quote_text.get_text(" ", strip=True))
        if author_text and author_text.get_text(strip=True):
            chunks.append(author_text.get_text(" ", strip=True))

    if chunks:
        return "\n".join(chunks)

    body_text = soup.get_text(" ", strip=True)
    return body_text


def build_inverted_index(pages: List[Dict[str, str]]) -> Dict[str, Any]:
    """Build inverted index with per-page frequency and token positions.

    Output shape:
    {
      "word": {
        "doc_freq": int,
        "pages": {
          "url": {"freq": int, "positions": [int, ...]}
        }
      }
    }
    """
    index: DefaultDict[str, Dict[str, Any]] = defaultdict(lambda: {"doc_freq": 0, "pages": {}})

    for page in pages:
        url = page["url"]
        text = _extract_page_text(page["html"])
        tokens = tokenize(text)

        local_positions: DefaultDict[str, List[int]] = defaultdict(list)
        for position, token in enumerate(tokens):
            local_positions[token].append(position)

        for token, positions in local_positions.items():
            entry = index[token]
            entry["pages"][url] = {
                "freq": len(positions),
                "positions": positions,
            }
            entry["doc_freq"] += 1

    return dict(sorted(index.items(), key=lambda kv: kv[0]))


def index_summary(index: Dict[str, Any]) -> Tuple[int, int]:
    """Return (distinct_terms, total_postings)."""
    distinct_terms = len(index)
    total_postings = sum(len(item["pages"]) for item in index.values())
    return distinct_terms, total_postings
